# Tuition Management System — Python + SQLite

import sqlite3
import datetime

# ── Database Setup ─────────────────────────────────────────────────────────────
def init_db():
    conn = sqlite3.connect("tuition.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            name      TEXT NOT NULL,
            subject   TEXT NOT NULL,
            grade     TEXT NOT NULL,
            phone     TEXT,
            fee       REAL NOT NULL,
            joined    TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            date       TEXT NOT NULL,
            status     TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS fees (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            month      TEXT NOT NULL,
            amount     REAL NOT NULL,
            paid       INTEGER DEFAULT 0,
            paid_date  TEXT,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS marks (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER NOT NULL,
            subject    TEXT NOT NULL,
            test_name  TEXT NOT NULL,
            marks      REAL NOT NULL,
            total      REAL NOT NULL,
            date       TEXT NOT NULL,
            FOREIGN KEY (student_id) REFERENCES students(id)
        )
    """)

    conn.commit()
    conn.close()


def get_conn():
    return sqlite3.connect("tuition.db")


# ── Helpers ────────────────────────────────────────────────────────────────────
def divider(title=""):
    if title:
        pad = (44 - len(title) - 2) // 2
        print("\n" + "─" * pad + f" {title} " + "─" * pad)
    else:
        print("─" * 46)

def today():
    return datetime.date.today().strftime("%Y-%m-%d")

def current_month():
    return datetime.date.today().strftime("%Y-%m")

def get_student_by_id(c, sid):
    c.execute("SELECT * FROM students WHERE id = ?", (sid,))
    return c.fetchone()

def list_all_students(c):
    c.execute("SELECT id, name, subject, grade FROM students ORDER BY name")
    rows = c.fetchall()
    if not rows:
        print("\n  No students enrolled yet.")
        return []
    print("\n  ID  Name                 Subject         Grade")
    divider()
    for r in rows:
        print(f"  {r[0]:<4}{r[1]:<21}{r[2]:<16}{r[3]}")
    divider()
    return rows


# ── 1. Student Management ──────────────────────────────────────────────────────
def add_student():
    divider("Add Student")
    name    = input("  Full Name    : ").strip()
    subject = input("  Subject      : ").strip()
    grade   = input("  Grade/Class  : ").strip()
    phone   = input("  Phone Number : ").strip()
    try:
        fee = float(input("  Monthly Fee  : ₹"))
    except ValueError:
        print("  Error: Invalid fee amount!")
        return

    if not name or not subject or not grade:
        print("  Error: Name, subject and grade are required!")
        return

    conn = get_conn()
    c = conn.cursor()
    c.execute(
        "INSERT INTO students (name, subject, grade, phone, fee, joined) VALUES (?,?,?,?,?,?)",
        (name, subject, grade, phone, fee, today())
    )
    conn.commit()
    sid = c.lastrowid
    conn.close()
    print(f"\n  ✅ Student added! ID: {sid}  Name: {name}")


def view_students():
    divider("All Students")
    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT id, name, subject, grade, phone, fee, joined FROM students ORDER BY name")
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("\n  No students enrolled yet.")
        return
    print(f"\n  {'ID':<5}{'Name':<20}{'Subject':<14}{'Grade':<8}{'Phone':<14}{'Fee':>8}  {'Joined'}")
    divider()
    for r in rows:
        print(f"  {r[0]:<5}{r[1]:<20}{r[2]:<14}{r[3]:<8}{r[4] or 'N/A':<14}₹{r[5]:>7.0f}  {r[6]}")
    divider()
    print(f"  Total students: {len(rows)}")


def delete_student():
    divider("Delete Student")
    conn = get_conn()
    c = conn.cursor()
    list_all_students(c)
    try:
        sid = int(input("\n  Enter Student ID to delete: "))
    except ValueError:
        print("  Error: Invalid ID!")
        conn.close()
        return
    student = get_student_by_id(c, sid)
    if not student:
        print("  Error: Student not found!")
        conn.close()
        return
    confirm = input(f"  Delete '{student[1]}'? This removes all their records. (yes/no): ").strip().lower()
    if confirm == "yes":
        c.execute("DELETE FROM attendance WHERE student_id = ?", (sid,))
        c.execute("DELETE FROM fees WHERE student_id = ?", (sid,))
        c.execute("DELETE FROM marks WHERE student_id = ?", (sid,))
        c.execute("DELETE FROM students WHERE id = ?", (sid,))
        conn.commit()
        print(f"  🗑️  Deleted student '{student[1]}' and all their records.")
    else:
        print("  Cancelled.")
    conn.close()


# ── 2. Attendance ──────────────────────────────────────────────────────────────
def mark_attendance():
    divider("Mark Attendance")
    conn = get_conn()
    c = conn.cursor()
    students = list_all_students(c)
    if not students:
        conn.close()
        return

    date = input(f"\n  Date (YYYY-MM-DD) [Enter for today: {today()}]: ").strip()
    if not date:
        date = today()

    print("\n  Mark each student:  P = Present  |  A = Absent  |  L = Leave")
    divider()
    for s in students:
        # Check if already marked
        c.execute("SELECT status FROM attendance WHERE student_id=? AND date=?", (s[0], date))
        existing = c.fetchone()
        if existing:
            print(f"  {s[1]:<22} Already marked: {existing[0]}")
            continue
        status = input(f"  {s[1]:<22} (P/A/L): ").strip().upper()
        if status not in ("P", "A", "L"):
            status = "A"
        c.execute("INSERT INTO attendance (student_id, date, status) VALUES (?,?,?)", (s[0], date, status))

    conn.commit()
    conn.close()
    print(f"\n  ✅ Attendance marked for {date}")


def view_attendance():
    divider("View Attendance")
    conn = get_conn()
    c = conn.cursor()
    students = list_all_students(c)
    if not students:
        conn.close()
        return

    try:
        sid = int(input("\n  Enter Student ID (0 for all): "))
    except ValueError:
        print("  Error: Invalid ID!")
        conn.close()
        return

    if sid == 0:
        c.execute("""
            SELECT s.name, a.date, a.status
            FROM attendance a
            JOIN students s ON s.id = a.student_id
            ORDER BY a.date DESC LIMIT 50
        """)
        rows = c.fetchall()
        print(f"\n  {'Name':<22}{'Date':<14}Status")
        divider()
        for r in rows:
            symbol = "✓" if r[2] == "P" else ("L" if r[2] == "L" else "✗")
            print(f"  {r[0]:<22}{r[1]:<14}{symbol} {r[2]}")
    else:
        student = get_student_by_id(c, sid)
        if not student:
            print("  Student not found!")
            conn.close()
            return
        c.execute("SELECT date, status FROM attendance WHERE student_id=? ORDER BY date DESC", (sid,))
        rows = c.fetchall()
        total     = len(rows)
        present   = sum(1 for r in rows if r[1] == "P")
        absent    = sum(1 for r in rows if r[1] == "A")
        on_leave  = sum(1 for r in rows if r[1] == "L")
        pct       = (present / total * 100) if total > 0 else 0

        print(f"\n  Student : {student[1]}")
        print(f"  Summary : {present}P  {absent}A  {on_leave}L  |  {pct:.1f}% attendance")
        divider()
        print(f"  {'Date':<14}Status")
        divider()
        for r in rows[:20]:
            symbol = "✓" if r[1] == "P" else ("L" if r[1] == "L" else "✗")
            print(f"  {r[0]:<14}{symbol} {r[1]}")

    conn.close()


# ── 3. Fee Management ──────────────────────────────────────────────────────────
def add_fee_record():
    divider("Add Fee Record")
    conn = get_conn()
    c = conn.cursor()
    list_all_students(c)
    try:
        sid = int(input("\n  Enter Student ID: "))
    except ValueError:
        print("  Error: Invalid ID!")
        conn.close()
        return

    student = get_student_by_id(c, sid)
    if not student:
        print("  Student not found!")
        conn.close()
        return

    month = input(f"  Month (YYYY-MM) [Enter for {current_month()}]: ").strip()
    if not month:
        month = current_month()

    try:
        amount = float(input(f"  Amount [Enter for ₹{student[5]:.0f}]: ₹") or student[5])
    except ValueError:
        amount = student[5]

    paid_input = input("  Mark as paid? (y/n): ").strip().lower()
    paid      = 1 if paid_input == "y" else 0
    paid_date = today() if paid == 1 else None

    c.execute(
        "INSERT INTO fees (student_id, month, amount, paid, paid_date) VALUES (?,?,?,?,?)",
        (sid, month, amount, paid, paid_date)
    )
    conn.commit()
    conn.close()
    status = "✅ Paid" if paid else "⏳ Pending"
    print(f"\n  Fee record added for {student[1]} — {month} — ₹{amount:.0f} — {status}")


def mark_fee_paid():
    divider("Mark Fee as Paid")
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT f.id, s.name, f.month, f.amount
        FROM fees f JOIN students s ON s.id = f.student_id
        WHERE f.paid = 0
        ORDER BY f.month
    """)
    rows = c.fetchall()
    if not rows:
        print("\n  🎉 No pending fees!")
        conn.close()
        return

    print(f"\n  {'ID':<6}{'Name':<22}{'Month':<12}Amount")
    divider()
    for r in rows:
        print(f"  {r[0]:<6}{r[1]:<22}{r[2]:<12}₹{r[3]:.0f}")
    divider()

    try:
        fid = int(input("\n  Enter Fee ID to mark as paid: "))
    except ValueError:
        print("  Error: Invalid ID!")
        conn.close()
        return

    c.execute("UPDATE fees SET paid=1, paid_date=? WHERE id=?", (today(), fid))
    conn.commit()
    conn.close()
    print("  ✅ Fee marked as paid!")


def view_fees():
    divider("Fee Summary")
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        SELECT s.name, f.month, f.amount, f.paid, f.paid_date
        FROM fees f JOIN students s ON s.id = f.student_id
        ORDER BY f.month DESC, s.name
    """)
    rows = c.fetchall()
    conn.close()
    if not rows:
        print("\n  No fee records found.")
        return

    total_collected = sum(r[2] for r in rows if r[3] == 1)
    total_pending   = sum(r[2] for r in rows if r[3] == 0)

    print(f"\n  {'Name':<22}{'Month':<12}{'Amount':>8}  {'Status':<10}Paid On")
    divider()
    for r in rows:
        status = "✅ Paid" if r[3] == 1 else "⏳ Pending"
        paid_on = r[4] or "—"
        print(f"  {r[0]:<22}{r[1]:<12}₹{r[2]:>7.0f}  {status:<10}{paid_on}")
    divider()
    print(f"  Collected : ₹{total_collected:.0f}")
    print(f"  Pending   : ₹{total_pending:.0f}")
    print(f"  Total     : ₹{total_collected + total_pending:.0f}")


# ── 4. Marks Management ────────────────────────────────────────────────────────
def add_marks():
    divider("Add Marks")
    conn = get_conn()
    c = conn.cursor()
    list_all_students(c)
    try:
        sid = int(input("\n  Enter Student ID: "))
    except ValueError:
        print("  Error: Invalid ID!")
        conn.close()
        return

    student = get_student_by_id(c, sid)
    if not student:
        print("  Student not found!")
        conn.close()
        return

    subject   = input(f"  Subject [Enter for {student[2]}]: ").strip() or student[2]
    test_name = input("  Test Name (e.g. Mock Test 1): ").strip()
    try:
        marks = float(input("  Marks Obtained : "))
        total = float(input("  Total Marks    : "))
    except ValueError:
        print("  Error: Invalid marks!")
        conn.close()
        return

    if marks > total:
        print("  Error: Marks cannot exceed total!")
        conn.close()
        return

    c.execute(
        "INSERT INTO marks (student_id, subject, test_name, marks, total, date) VALUES (?,?,?,?,?,?)",
        (sid, subject, test_name, marks, total, today())
    )
    conn.commit()
    conn.close()
    pct = marks / total * 100
    print(f"\n  ✅ Marks added! {student[1]} scored {marks}/{total} ({pct:.1f}%) in {test_name}")


def view_marks():
    divider("View Marks")
    conn = get_conn()
    c = conn.cursor()
    students = list_all_students(c)
    if not students:
        conn.close()
        return
    try:
        sid = int(input("\n  Enter Student ID: "))
    except ValueError:
        print("  Error: Invalid ID!")
        conn.close()
        return

    student = get_student_by_id(c, sid)
    if not student:
        print("  Student not found!")
        conn.close()
        return

    c.execute("SELECT subject, test_name, marks, total, date FROM marks WHERE student_id=? ORDER BY date DESC", (sid,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        print(f"\n  No marks recorded for {student[1]}.")
        return

    print(f"\n  Student: {student[1]}")
    print(f"\n  {'Subject':<16}{'Test':<22}{'Marks':>7}{'Total':>7}{'%':>8}  Date")
    divider()
    for r in rows:
        pct = r[2] / r[3] * 100
        grade = "A+" if pct>=90 else "A" if pct>=80 else "B" if pct>=70 else "C" if pct>=60 else "D" if pct>=50 else "F"
        print(f"  {r[0]:<16}{r[1]:<22}{r[2]:>7.1f}{r[3]:>7.1f}{pct:>7.1f}%  {r[4]}  {grade}")
    divider()
    avg = sum(r[2]/r[3]*100 for r in rows) / len(rows)
    print(f"  Average: {avg:.1f}%")


# ── 5. Dashboard ───────────────────────────────────────────────────────────────
def dashboard():
    divider("Dashboard")
    conn = get_conn()
    c = conn.cursor()

    c.execute("SELECT COUNT(*) FROM students")
    total_students = c.fetchone()[0]

    c.execute("SELECT COUNT(*), SUM(amount) FROM fees WHERE paid=1")
    row = c.fetchone()
    fees_collected = row[1] or 0

    c.execute("SELECT COUNT(*), SUM(amount) FROM fees WHERE paid=0")
    row = c.fetchone()
    fees_pending = row[1] or 0

    c.execute("SELECT COUNT(*) FROM attendance WHERE date=? AND status='P'", (today(),))
    present_today = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM attendance WHERE date=?", (today(),))
    marked_today = c.fetchone()[0]

    print(f"\n  📅 Date           : {today()}")
    print(f"  👨‍🎓 Total Students : {total_students}")
    print(f"  ✅ Present Today  : {present_today}/{marked_today} marked")
    print(f"  💰 Fees Collected : ₹{fees_collected:.0f}")
    print(f"  ⏳ Fees Pending   : ₹{fees_pending:.0f}")

    # Top performers
    c.execute("""
        SELECT s.name, AVG(m.marks * 100.0 / m.total) as avg_pct
        FROM marks m JOIN students s ON s.id = m.student_id
        GROUP BY m.student_id ORDER BY avg_pct DESC LIMIT 3
    """)
    top = c.fetchall()
    if top:
        print(f"\n  🏆 Top Performers:")
        for i, t in enumerate(top, 1):
            print(f"     {i}. {t[0]:<20} {t[1]:.1f}%")

    conn.close()


# ── Main Menu ──────────────────────────────────────────────────────────────────
def main():
    init_db()
    print("=" * 46)
    print("       🎓 TUITION MANAGEMENT SYSTEM")
    print("=" * 46)

    menus = {
        "1": ("👨‍🎓 Student Management", {
            "1": ("Add Student",    add_student),
            "2": ("View Students",  view_students),
            "3": ("Delete Student", delete_student),
        }),
        "2": ("📋 Attendance", {
            "1": ("Mark Attendance", mark_attendance),
            "2": ("View Attendance", view_attendance),
        }),
        "3": ("💰 Fee Management", {
            "1": ("Add Fee Record",  add_fee_record),
            "2": ("Mark Fee Paid",   mark_fee_paid),
            "3": ("View All Fees",   view_fees),
        }),
        "4": ("📝 Marks & Tests", {
            "1": ("Add Marks",  add_marks),
            "2": ("View Marks", view_marks),
        }),
        "5": ("📊 Dashboard", None),
        "6": ("🚪 Exit",       None),
    }

    while True:
        print("\n  MAIN MENU")
        divider()
        for key, val in menus.items():
            print(f"  {key}. {val[0]}")
        divider()

        choice = input("  Choose (1-6): ").strip()

        if choice == "5":
            dashboard()
        elif choice == "6":
            print("\n  Goodbye! 👋\n")
            break
        elif choice in menus and menus[choice][1]:
            sub = menus[choice][1]
            print(f"\n  {menus[choice][0]}")
            divider()
            for k, v in sub.items():
                print(f"  {k}. {v[0]}")
            divider()
            sub_choice = input("  Choose: ").strip()
            if sub_choice in sub:
                sub[sub_choice][1]()
            else:
                print("  Invalid choice!")
        else:
            print("  Invalid choice!")

if __name__ == "__main__":
    main()
