from pptx import Presentation

def create_presentation():
    while True:
        try:
            num_slides = int(input("Hvor mange slides vil du ha i presentasjonen? "))
            prs_title = input("Hva skal presentasjonen hete? ")
            print(f"Du har valgt å lage en presentasjon med {num_slides} slides.")
            break
        except ValueError:
            print("Vennligst skriv inn et gyldig tall.")

            prs = Presentation()

            for i in range(num_slides):
                slide_layout = prs.slide_layouts[0] # Velger en enkel layout for hver slide
                slide = prs.slides.add_slide(slide_layout)
                title = slide.shapes.title
                title.text = f"Slide {i + 1}"
            prs.save(f"{prs_title}.pptx")
            print(f"Presentasjonen er lagret som '{prs_title}.pptx'.")


create_presentation()