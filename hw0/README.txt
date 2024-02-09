Iselda Aiello

This message was encrypted using a polyalphabetic cipher, or a Vigenere-esque cipher using three different monoalphabetic ciphers.

I first thought that there would be three Caesar ciphers, however quickly realized this wasn't the case when I went to test a shifted alphabet on the encrypted text. Then, I had decided to create three separate alphabets and decoded the words "welcome to cryptography." I then used these letters to decipher more words until I had deciphered the text.
I wrote out a C program to help speed up the process for me. Originally, I created an offset variable for the Caesar cipher approach and offset each letter in the plaintext. This is when I realized this approach wouldn't work. That's when I decided to create three separate alphabets and "decode" the message by hand.
The final C program I used to decipher the text is bundled with this README in the attached tarball.
