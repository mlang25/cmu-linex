import requests

res_logo_links = {
    "0": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/ABP_Logo_wTagline_onwht.jpg",
    "1": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/BackBarGrill-Logo.jpg",
    "2": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/logo.jpg",
    "3": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/CMCafeLogo.png",
    "4": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/Cucina_Logo.jpg",
    "5": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/ExchangeLogoDistressWhiteFill.jpg",
    "6": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/Fresh52Logo1.png",
    "7": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/El-Gallo-de-Oro_Logo.fw.png",
    "8": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/grano-logo-min.png",
    "9": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/hunan-express-logo-min3.jpg",
    "10": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/InnovationKitchenLogo.png",
    "11": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/LaPrima_Seal_black.png",
    "12": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/RothbergsRoasters_logo.png",
    "13": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/script-pink%20(1).png",
    "14": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/NourishLogoNoTagline_2018_revision.png",
    "15": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/La%20Prima%20Social.png",
    "16": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/temp%20logo_tagline.png",
    "17": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/Rooted-Logo.jpg",
    "18": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/cropped%20on%20the%20edges.jpg",
    "19": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/SchatzLogocropped.jpg",
    "20": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/TahiniLogo-WithTagAndBowlArt.png",
    "21": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/TasteOfIndiaLogo.png",
    "22": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/UG-Mark_Secondary_Brown.jpg",
    "23": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/urban%20revolution.png",
    "24": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/wildbluelogo.png",
    "25": "https://apps.studentaffairs.cmu.edu/dining/conceptinfo/conceptAssets/logos/ZebraLounge%202400r300.jpg",
}

if __name__ == "__main__":
    for i, link in res_logo_links.items():
        print(i, link)
        img_data = requests.get(link).content
        with open(f"logos/{i}.{link[-3:]}", "wb") as file:
            file.write(img_data)
