def caesar_cipher(text, shift, mode="encrypt"):
    result = ""
    
    # Reverse shift for decryption
    if mode == "decrypt":
        shift = -shift
    
    for char in text:
        if char.isalpha():
            # Preserve case
            base = ord('A') if char.isupper() else ord('a')
            shifted = (ord(char) - base + shift) % 26 + base
            result += chr(shifted)
        else:
            # Keep spaces, numbers, symbols unchanged
            result += char
    
    return result


def main():
    print("🔐 Caesar Cipher Tool")
    
    while True:
        mode = input("\nChoose mode (encrypt/decrypt): ").lower()
        if mode not in ["encrypt", "decrypt"]:
            print("Invalid mode. Try again.")
            continue
        
        text = input("Enter your message: ")
        
        try:
            shift = int(input("Enter shift value (number): "))
        except ValueError:
            print("Invalid shift. Must be a number.")
            continue
        
        output = caesar_cipher(text, shift, mode)
        
        print(f"\nResult: {output}")
        
        again = input("\nDo you want to continue? (y/n): ").lower()
        if again != 'y':
            print("Goodbye! 👋")
            break


if __name__ == "__main__":
    main()
