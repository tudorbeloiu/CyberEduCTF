Categorie: pwn (Binary Exploitation)
Link catre challenge: https://app.cyber-edu.co/challenges/08ef6340-c1e4-11eb-9b9f-6bd8e9c6de87/?tenant=cyberedu

Am descarcat executabilul pe care ni-l da challenge-ul si am aflat detalii despre el:
    /img/filedesc.png

Este un program pe 32 de biti, ordinea in memorie este little-endian(o sa avem nevoie de informatia asta pentru scrierea payload-ului) si alte informatii interesante dar care nu ne influenteaza rezolvarea cerintei.


Am rulat programul si am aflat informatii care probabil o sa ne fie de ajutor mai incolo:
    /img/rulare.png

    "Value to break is at 0x0804a030 and has a hex value 0x0000000a".

Codul functiei main decompilat in ghidra:
    /img/main.png

![Codul decompilat al funcției printFlag](img/printflag.png)

Funcția `printFlag` este simplă: execută un apel de sistem `execve` pentru a rula `/usr/bin/cat flag.txt`, afișând astfel conținutul flag-ului.


Challenge ul este de tipul format string vulnerability din cauza printf ului

    strlcat(local_1b0,local_e8,200);
    printf(local_1b0);
    puVar2 = &demo.3187;
    iVar1 = demo.3187;

Obiectivul este sa suprascriem valoarea de la adresa 0x804a030(corespunzatoare lui demo3147) cu valoarea 0x20 pentru a putea intra pe ramura de if care apeleaza functia printflag.

Am vizualizat codul de assembly din debugger folosind comanda gdb format. 
Am rulat disass main pentru a vedea zona printf ului: 
    /img/memorie.png 
     
Am dat un break la instructiunea executata dinaintea printf ului nostru si am inspectat

valorile de pe stiva de la momentul respectiv:
    /img/stiva.png

Putem observa ca pe stiva incepand cu adresa 0xffffcc70 este sirul nostru local_1b0, format din concatenarea lui "Break stuff.  " si a sirului introdus de noi, "AAAA": 
    builtin_strncpy(local_1b0,"Break stuff.  ",0xf);
    strlcat(local_1b0,local_e8,200);
    unde local_e8 este sirul introdus la tastatura: fgets(local_e8,200,_stdin)


Pentru a scrie la o adresă, trebuie să folosim specificantul %n. Pentru a scrie la o adresă specifică de pe stivă, folosim argumente poziționale (de ex. %8$n). Trebuie să găsim indexul (N) corect.
La adresa respectiva (0x0804a030) se va scrie numarul de bytes afisati pana la intalnirea lui %n.


Acum trebuie doar sa aliniam adresa tinta 0x804a030 pe stiva.
String ul "Break stuff.  " are deja 14 caractere(cu tot cu cele 2 spatii de la final), deci trebuie sa mai adaugam inca 18 bytes la payload, dintre care 4 sunt adresa in format little endian "\x30\xa0\x04\x08". Mai adaugam inca 14 bytes de caractere nope "\x90" si observam stiva la momentul apelului printf:

    /img/farapadd.png

Din cauza celor 2 spatii de la finalul lui "Break stuff.  " trebuie sa adaugam 2 bytes de padding inainte si pastram doar 12 bytes de padding dupa ce scriem adresa:

    /img/corect.png

Acum, adresa la care trebuie sa scriem noua valoare se afla pe stiva la adresa 0xffffcc80 si este al 8-lea argument de pe stiva. Deci, in payload folosim %8$n pentru a scrie la al 8-lea argument de pe stiva:
    /img/flaggdb.png

Ok, pare ca functioneaza, e timpul sa trimitem payload ul si la server ul challenge ului ca sa ne dea continutul lui flag.txt:

    /img/flag.jpg




