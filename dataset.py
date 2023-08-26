import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk
import customtkinter as ck
import random
import numpy as np

easySet = ["The cat sat on the mat, purring softly as it basked in the warm sunlight. The room was quiet and peaceful, perfect for a lazy afternoon nap.",
                "The sky was blue and clear, with fluffy white clouds drifting lazily by. A gentle breeze blew, making it a great day for a picnic in the park.",
                "A friendly dog wagged its tail as it approached, eager to make new friends. The children laughed and played with the happy pup.",
                "The sun shone brightly on the flowers in the garden, their vibrant colors creating a beautiful scene. Bees buzzed around, collecting nectar.",
                "A group of friends gathered by the lake, sharing stories and laughter. They enjoyed the cool water and the warm sun on their skin."]

mildSet = ["As the sun slowly rose over the horizon, the morning dew began to evaporate, creating a magical mist that filled the air. Birds chirped cheerfully in the distance, and a gentle breeze blew through the trees, rustling the leaves. It was the perfect day to take a leisurely stroll through the park and enjoy the beauty of nature.",
                    "The smell of freshly brewed coffee wafted through the air, beckoning me to the kitchen. I poured myself a cup and sipped the hot, bitter liquid, savoring the taste. The morning paper lay on the table, waiting to be read. I scanned the headlines and frowned at the latest news. It was going to be a long day.",
                    "The waves crashed against the shore, sending salty spray into the air. The sand was warm beneath my feet, and I breathed in the salty scent of the ocean. Seagulls cried overhead, diving and soaring in the blue sky. It was a beautiful day to be at the beach.",
                    "The sound of laughter echoed through the park, as children played on the swings and slides. Parents sat on benches, chatting and watching their kids. A dog barked excitedly, chasing a ball. The sun shone down, warming everything in its path. It was a perfect day for a family outing.",
                    "The city streets were bustling with activity, as people hurried to work or school. Cars honked and buses roared, creating a cacophony of noise. Pedestrians jostled for space on the crowded sidewalks, dodging each other as they rushed by. It was a typical day in the city."]

difficultSet = ["Simultaneously, the xylophonist struck a dissonant chord, the mime traipsed across the stage, and the unicyclist juggled flaming torches. The audience, entranced, oscillated between gasps and applause as the surreal spectacle unfolded before their eyes.",
                    "Perusing the cacophony of knick-knacks that cluttered the antiquarian's shop, I stumbled upon a peculiar, oblong contraption with an array of switches and dials. An enigmatic aura emanated from it, piquing my curiosity and compelling me to investigate further.",
                    "The cloying, saccharine scent of the candy factory wafted through the air, permeating the atmosphere with notes of caramel, nougat, and a hint of marzipan. Workers, clad in aprons and hairnets, bustled about, crafting confections in a mesmerizing display of sweet alchemy.",
                    "Navigating the labyrinthine alleyways of the ancient city, I stumbled upon an esoteric bazaar, replete with mysterious trinkets and enigmatic wares. A cacophony of languages filled the air, creating a dizzying symphony of conversation and bartering.",
                    "Amidst the plethora of flora and fauna, the intricate dance of life unfolded in the verdant jungle. Epiphytes clung to towering trees, while iridescent insects skittered across the damp forest floor. The cacophony of calls from arboreal dwellers punctuated the air, composing an orchestral symphony of nature."]

extremeSet = ["The tempestuous maelstrom—torrential rain, howling winds, and lightning fracturing the sky—assailed the beleaguered vessel, its beleaguered crew valiantly navigating betwixt churning waves; Poseidon's wrath, it seemed, knew no bounds.",
                    "As the clock struck midnight, the cacophony of revelers crescendoed; fireworks burst overhead, illuminating the sky with kaleidoscopic hues, whilst a myriad of languages melded in harmonious exultation—welcoming a new year with fervent enthusiasm.",
                    "In the chiaroscuro of the dimly lit chamber, an assemblage of eclectic artifacts (ranging from cryptic manuscripts to archaic relics) lay strewn haphazardly, each imbued with esoteric properties that beguiled even the most seasoned of occult scholars.",
                    "Trepidation gripped her as she traversed the phantasmagoric dreamscape, where grotesque amalgamations of flora and fauna—a serpentine arboreal creature slithering betwixt shadows; a chimeric, multi-limbed beast, galumphing clumsily—stalked the liminal realm.",
                    "The grandiloquent orator—gesticulating theatrically and wielding an array of sesquipedalian verbiage—enthralled his audience, beguiling them with a panoply of grandiose claims and rhetorical flourishes that rendered the veracity of his assertions nigh indiscernible."]
cars = [("car", 0), ("monster_truck", 2000), ("lambo", 9900)]

turns = [[0.88, 0.65],
        [0.88, 0.4],
        [0.64, 0.4],
        [0.64, 0.16],
        [0.25, 0.16],
        [0.25, 0.37],
        [0.10, 0.37],
        [0.10, 0.77],
        [0.88, 0.77],
        [0.88, 0.65]]

turnArray = np.array(turns)

def getTurns():
    return turnArray

def getCars():
    return cars

def returnSentence(difficulty):
    if (difficulty == "Easy"):
        return random.choice(easySet)
    if (difficulty == "Mild"):
        return random.choice(mildSet)
    if (difficulty == "Difficult"):
        return random.choice(difficultSet)
    if (difficulty == "Extreme"):
        return random.choice(extremeSet)
