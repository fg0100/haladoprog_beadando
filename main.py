import sys
import string
from PIL import Image, ImageOps

# bemenet átalakítása
def color_input(text):
    
    text = text.strip()
    if not text:
        raise ValueError("Nem adott meg színt!")

    szin = text.replace(",", " ").split()
    if len(szin) != 3:
        raise ValueError("Használja az 'R G B' formátumot!")

    #integerré alakítás
    r, g, b = map(int, szin)
    if any(not 0 <= v <= 255 for v in (r, g, b)):
        raise ValueError("Az értékeknek 0 és 255 között kell lenniük")
    return r, g, b

#színkód újra megadásának lehetősége
def color_prompt(prompt):
    while True:
        user_input = input(prompt)
        try:
            return color_input(user_input)
        except ValueError as e:
            print(f"Nem megfelelő színkód: {e}")
            ujra = input("Megpróbálja újra? (i/n): ").strip().lower()
            if ujra != "i":
                sys.exit("Kilépés.")

#kicseréli az src_colort a dst_colorra
def replace_color(img, src_color, dst_color, tolerance):
   
    tolerance = max(0, int(tolerance))
    tol2 = tolerance * tolerance
    src_r, src_g, src_b = src_color
    dst_r, dst_g, dst_b = dst_color

    img = img.convert("RGBA")
    pixel = []
    for r, g, b, a in img.getdata():
        dr = r - src_r
        dg = g - src_g
        db = b - src_b
        if dr * dr + dg * dg + db * db <= tol2:
            pixel.append((dst_r, dst_g, dst_b, a))
        else:
            pixel.append((r, g, b, a))

    img.putdata(pixel)
    return img


def main():
    print("\n\n")
    path = input("Add meg a kép helyét és nevét: ").strip().strip('"')
    if not path:
        sys.exit("Hiba: a kép helye nem lehet üres!")

    try:
        img = Image.open(path)
        print(f"Loaded image '{path}' (mód: {img.mode}, méret: {img.size[0]}x{img.size[1]})")
    except Exception as e:
        sys.exit(f"Hiba: a képet nem lehetett megnyitni!: {e}")

    print("\nVálassza ki mit akar tenni:")
    print(" 1) Szín csere")
    print(" 2) Szürke árnyalatosítás")
    print(" 3) Színek invertálás")

    choice = input("Írjon 1-et, 2-t, 3-at: ").strip()
    while choice not in {"1", "2", "3"}:
        choice = input("Hiba: csak 1,2 és 3 lehet a bemenet: ").strip()

    if choice == "1":
        print("\nSzín csere")
        
        #színek bekérése
        src_color = color_prompt("Adja meg a cserélni kívánt színt(R,G,B): ")
        dst_color = color_prompt("Adja meg a színt amire cserélni szeretnéd(R,G,B): ")

        #tolerancia  bekérése és 
        tol_default = 40
        tol_input = input(f"Adja meg a tolerancia értékét(0–255, Nyomjon entert, ha maradjon ({tol_default}): ").strip()
        try:
            tolerance = int(tol_input) if tol_input else tol_default
        except ValueError:
            print(f"Hiba: rosszul megadott tolerancia érték, az alap értékkel folytatódik a program: {tol_default}.")
            tolerance = tol_default

        print("Szín cseréje...")
        result_img = replace_color(img, src_color, dst_color, tolerance)

    elif choice == "2":
        print("\nSzürke árnyalatos")
        result_img = ImageOps.grayscale(img)

    else:
        print("\nSzínek invertálás")
        # megtartjuk az alphát, ha van
        if img.mode == "RGBA":
            r, g, b, a = img.split()
            rgb = Image.merge("RGB", (r, g, b))
            inv = ImageOps.invert(rgb)
            r2, g2, b2 = inv.split()
            result_img = Image.merge("RGBA", (r2, g2, b2, a))
        else:
            result_img = ImageOps.invert(img.convert("RGB"))

    output_path = input("\nAdja meg a kép kimenetének helyét és nevét: ").strip().strip('"')
    if not output_path:
        sys.exit("Hiba: a kimenet helye nem lehet üres!")

    try:
        result_img.save(output_path)
        print(f"A kép sikeresen mentésre került: '{output_path}'.")
    except Exception as e:
        print(f"Hiba: nem lehetett elmenteni a képet: {e}")


if __name__ == "__main__":
    main()
