import sqlite3
from query_engine.code.model import model
import re
import time
from query_engine.code.uniform_sampling import simple_query_engine
import random
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor


# Insert sample data
data = [
    (1, "John Doe is a software engineer at Google in Mountain View, California."),
    (2, "Microsoft, headquartered in Redmond, Washington, was founded by Bill Gates and Paul Allen."),
    (3, "Barack Obama was the 44th president of the United States."),
    (4, "The Eiffel Tower is located in Paris, France."),
    (5, "The Great Wall of China is a UNESCO World Heritage site."),
    (6, "Apple Inc. is an American multinational technology company headquartered in Cupertino, California."),
    (7, "The Statue of Liberty is a famous landmark in New York City, USA."),
    (8, "Leonardo da Vinci was an Italian artist, scientist, and inventor during the Renaissance."),
    (9, "The United Nations is an international organization founded in 1945 to promote peace and cooperation."),
    (10, "Amazon is an e-commerce company founded by Jeff Bezos in 1994."),
    (11, "Mount Everest, located in the Himalayas, is the highest peak in the world."),
    (12, "The Louvre Museum in Paris, France, is home to the famous painting, the Mona Lisa."),
    (13, "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity."),
    (14, "The Grand Canyon is a famous natural landmark located in Arizona, USA."),
    (15, "J.K. Rowling is a British author best known for writing the Harry Potter series."),
    (16, "The Great Barrier Reef, located off the coast of Queensland, Australia, is the world's largest coral reef system."),
    (17, "Nelson Mandela was a South African anti-apartheid revolutionary, political leader, and philanthropist who served as President of South Africa from 1994 to 1999."),
    (18, "Tokyo, the capital city of Japan, is one of the most populous cities in the world."),
    (19, "Facebook, a social media platform, was founded by Mark Zuckerberg in 2004."),
    (20, "The Colosseum, an ancient Roman amphitheater, is located in Rome, Italy."),
    (21, "Marie Curie was a Polish-born physicist and chemist who conducted pioneering research on radioactivity."),
    (22, "The Great Pyramid of Giza is the oldest and largest of the three pyramids in Giza, Egypt."),
    (23, "Walt Disney was an American entrepreneur, animator, and film producer, who co-founded the Walt Disney Company."),
    (24, "The Taj Mahal, an ivory-white marble mausoleum, is located in Agra, India."),
    (25, "Thomas Edison, an American inventor and businessman, is best known for inventing the light bulb."),
    (26, "Niagara Falls is a group of three waterfalls located on the border of Ontario, Canada, and New York, United States."),
    (27, "Isaac Newton was an English mathematician, physicist, and astronomer, who is widely recognized as one of the most influential scientists of all time."),
    (28, "The Great Sphinx of Giza is a large limestone statue located on the Giza Plateau in Egypt."),
    (29, "Twitter is a social media platform founded by Jack Dorsey, Biz Stone, and Evan Williams in 2006."),
    (30, "The Leaning Tower of Pisa is a famous architectural landmark in Pisa, Italy."),
    (31, "Charles Darwin was a British naturalist who developed the theory of evolution through natural selection."),
    (32, "Machu Picchu is an ancient Incan citadel located in the Andes Mountains in Peru."),
    (33, "The Sydney Opera House is a famous performing arts venue in Sydney, Australia."),
    (34, "Jane Austen was an English novelist known for her works such as Pride and Prejudice and Sense and Sensibility."),
    (35, "The London Eye is a giant Ferris wheel located on the South Bank of the River Thames in London, England."),
    (36, "Pablo Picasso was a Spanish painter, sculptor, printmaker, and ceramicist, known for co-founding the Cubist movement."),
    (37, "The Great Ocean Road is a scenic coastal drive along the southeastern coast of Australia."),
    (38, "Galileo Galilei was an Italian astronomer, physicist, and engineer, who played a major role in the scientific revolution."),
    (39, "Big Ben is a famous clock tower located at the north end of the Palace of Westminster in London, United Kingdom."),
    (40, "Steve Jobs was an American entrepreneur and co-founder of Apple Inc."),
    (41, "The Acropolis of Athens is an ancient citadel located on a rocky outcrop above the city of Athens, Greece."),
    (42, "Mother Teresa was an Albanian-Indian Roman Catholic nun and missionary, who dedicated her life to helping the poor."),
    (43, "The Golden Gate Bridge is a suspension bridge that spans the Golden Gate Strait in San Francisco, California."),
    (44, "Vincent van Gogh was a Dutch painter, known for his works such as The Starry Night and Sunflowers."),
    (45, "The Amazon Rainforest is a vast tropical rainforest located in the Amazon Basin of South America."),
    (46, "Mahatma Gandhi was an Indian leader who led India to independence from British rule through nonviolent civil disobedience."),
    (47, "The Great Lakes are a series of interconnected freshwater lakes located primarily in the upper mid-east region of North America."),
    (48, "Maya Angelou was an American poet, singer, memoirist, and civil rights activist."),
    (49, "The Burj Khalifa is the tallest building in the world, located in Dubai, United Arab Emirates."),
    (50, "Martin Luther King Jr. was an American civil rights activist who fought for the advancement of civil rights for African Americans."),
    (51, "Marie Curie was a Polish-born physicist and chemist who conducted pioneering research on radioactivity."),
    (52, "The Leaning Tower of Pisa is a famous architectural landmark in Pisa, Italy, known for its unintended tilt."),
    (53, "The Grand Canyon is a steep-sided canyon carved by the Colorado River in Arizona, United States."),
    (54, "Pablo Picasso was a Spanish painter, sculptor, and printmaker, known for his contributions to the development of modern art."),
    (55, "The Great Barrier Reef is the world's largest coral reef system, located off the coast of Queensland, Australia."),
    (56, "Nelson Mandela was a South African anti-apartheid revolutionary, political leader, and philanthropist who served as President of South Africa."),
    (57, "The Louvre Museum is a historic monument and the world's largest art museum, located in Paris, France."),
    (58, "Machu Picchu is a 15th-century Inca citadel situated in the Eastern Cordillera of southern Peru."),
    (59, "William Shakespeare was an English playwright, poet, and actor, widely regarded as the greatest writer in the English language."),
    (60, "Niagara Falls is a group of three waterfalls at the southern end of Niagara Gorge, spanning the border between the US and Canada."),
    (61, "The Sydney Opera House is a multi-venue performing arts center in Sydney, Australia, known for its distinctive sail-like design."),
    (62, "Charles Darwin was an English naturalist, geologist, and biologist, best known for his theory of evolution by natural selection."),
    (63, "The Colosseum is an ancient Roman amphitheater located in Rome, Italy, and is the largest amphitheater ever built."),
    (64, "Frida Kahlo was a Mexican painter known for her self-portraits and works inspired by the nature and artifacts of Mexico."),
    (65, "Mount Everest is Earth's highest mountain above sea level, located in the Himalayas between Nepal and China."),
    (66, "Walt Disney was an American entrepreneur, animator, and film producer, who co-founded the Walt Disney Company."),
    (67, "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor, a symbol of freedom and democracy."),
    (68, "Jane Austen was an English novelist known for her works such as Pride and Prejudice, Sense and Sensibility, and Emma."),
    (69, "The Pyramids of Giza are ancient Egyptian pyramids, which are among the oldest and largest pyramids in the world."),
    (70, "Galileo Galilei was an Italian astronomer, physicist, and engineer, who played a significant role in the scientific revolution."),
    (71, "The Taj Mahal is an ivory-white marble mausoleum in Agra, India, built by Mughal Emperor Shah Jahan to house the tomb of his wife."),
    (72, "Sigmund Freud was an Austrian neurologist and the founder of psychoanalysis, a clinical method for treating psychopathology."),
    (73, "The Great Sphinx of Giza is a limestone statue of a reclining sphinx, a mythical creature with the body of a lion and the head of a human."),
    (74, "Wolfgang Amadeus Mozart was a prolific and influential composer of the Classical era, who composed over 600 works."),
    (75, "Alexander the Great was a king of Macedonia who conquered an empire that stretched from the Balkans to modern-day Pakistan."),
    (76, "Albert Einstein was a German-born theoretical physicist who developed the theory of relativity and the mass-energy equivalence formula, E=mc²."),
    (77, "The Roman Forum is a rectangular forum surrounded by the ruins of several important ancient government buildings in the center of Rome."),
    (78, "Amelia Earhart was an American aviation pioneer and author, the first female aviator to fly solo across the Atlantic Ocean."),
    (79, "The Acropolis of Athens is an ancient citadel located on a rocky outcrop above the city of Athens, containing the remains of several ancient buildings."),
    (80, "Leonardo da Vinci was an Italian polymath, known for his works in painting, sculpture, architecture, science, and mathematics."),
    (81, "The Empire State Building is a 102-story Art Deco skyscraper in Midtown Manhattan, New York City."),
    (82, "Isaac Newton was an English mathematician, physicist, and astronomer, who formulated the laws of motion and universal gravitation."),
    (83, "The Palace of Versailles is a royal chateau in Versailles, France, which was the principal residence of the French kings from the late 17th century."),
    (84, "Theodore Roosevelt was the 26th President of the United States, a statesman, and a leader of the Republican Party."),
    (85, "The Serengeti National Park is a Tanzanian national park in the Serengeti ecosystem, known for its annual migration of over 1.5 million wildebeest."),
    (86, "Cleopatra was the last active ruler of the Ptolemaic Kingdom of Egypt, and is best known for her love affairs with Julius Caesar and Mark Antony."),
    (87, "The Colossus of Rhodes was a statue of the Greek sun-god Helios, erected in the city of Rhodes, and considered one of the Seven Wonders of the Ancient World."),
    (88, "Rosa Parks was an American civil rights activist, who played a pivotal role in the Montgomery Bus Boycott."),
    (89, "The Great Ocean Road is a 243-kilometer-long road along the southeast coast of Australia, known for its scenic views and unique rock formations."),
    (90, "Thomas Edison was an American inventor and businessman, known for inventing the light bulb, phonograph, and motion picture camera."),
    (91, "The Hanging Gardens of Babylon were one of the Seven Wonders of the Ancient World, a series of tiered gardens containing various trees and plants."),
    (92, "Benjamin Franklin was an American polymath, statesman, and one of the Founding Fathers of the United States."),
    (93, "Petra is a historical and archaeological city in southern Jordan, known for its rock-cut architecture and water conduit system."),
    (94, "Emily Dickinson was an American poet, known for her reclusive lifestyle and unconventional use of language and syntax in her poetry."),
    (95, "The CN Tower is a 553.3-meter-high concrete communications and observation tower located in downtown Toronto, Canada."),
    (96, "Charles Dickens was an English writer and social critic, known for his novels such as Oliver Twist, A Tale of Two Cities, and Great Expectations."),
    (97, "The Berlin Wall was a guarded concrete barrier that divided Berlin from 1961 to 1989, a symbol of the Cold War."),
    (98, "The Great Wall of China is a series of fortifications built along the northern borders of China to protect against invasions."),
    (99, "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France, and is one of the most recognized landmarks in the world."),
    (100, "The Colosseum is an amphitheatre in Rome, Italy, and is considered one of the greatest works of Roman architecture and engineering."),
    (101, "The Taj Mahal is a white marble mausoleum in Agra, India, and is widely considered one of the most beautiful buildings in the world."),
    (102, "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor within New York City, in the United States."),
    (103, "The Great Pyramid of Giza is the oldest and largest of the three pyramids in the Giza pyramid complex in Egypt."),
    (104, "The Golden Gate Bridge is a suspension bridge spanning the Golden Gate strait, the mile-wide, three-mile-long channel between San Francisco Bay and the Pacific Ocean."),
    (105, "The Acropolis of Athens is an ancient citadel located on a rocky outcrop above the city of Athens and contains several ancient buildings of great architectural and historic significance."),
    (106, "Machu Picchu is an Incan citadel set high in the Andes Mountains in Peru, renowned for its sophisticated dry-stone walls that fuse huge blocks without the use of mortar."),
    (107, "The Pyramids of Teotihuacan are ancient Mesoamerican pyramids located in the Basin of Mexico, near the city of Teotihuacan."),
    (108, "Angkor Wat is a temple complex in Cambodia and is the largest religious monument in the world."),
    (109, "Stonehenge is a prehistoric monument located in Wiltshire, England and is one of the most famous prehistoric sites in the world."),
    (110, "The Christ the Redeemer statue is an Art Deco statue of Jesus Christ in Rio de Janeiro, Brazil, and is considered the largest Art Deco statue in the world."),
    (111, "The Sagrada Familia is a large unfinished Roman Catholic church in Barcelona, Spain, designed by Catalan architect Antoni Gaudí."),
    (112, "The Parthenon is a former temple on the Athenian Acropolis, Greece, dedicated to the goddess Athena, whom the people of Athens considered their patron."),
    (113, "The Forbidden City is a palace complex in central Beijing, China, and was the former Chinese imperial palace from the Ming dynasty to the end of the Qing dynasty."),
    (114, "Chichen Itza is a complex of Mayan ruins on Mexico's Yucatan Peninsula and includes the Pyramid of Kukulcan, a large stone structure with staircases up each of its four sides."),
    (115, "The Tower Bridge is a combined bascule and suspension bridge in London, England, over the River Thames."),
    (116, "The Louvre Museum is the world's largest art museum and a historic monument in Paris, France."),
    (117, "The Kremlin is a fortified complex in the center of Moscow, Russia, and includes four palaces, four cathedrals, and the enclosing Kremlin Wall with Kremlin towers."),
    (118, "The Alhambra is a palace and fortress complex in Granada, Spain, and was originally constructed as a small fortress in AD 889."),   
    (118, "The human brain has about 100 billion neurons."),
    (119, "The tallest building in the world is the Burj Khalifa in Dubai, which is 828 meters tall."),
    (120, "Mount Everest is the highest mountain in the world, with a peak reaching 8,848 meters above sea level."),
    (121, "The Great Barrier Reef is the world's largest coral reef system, composed of over 2,900 individual reefs."),
    (122, "The United States has the world's largest economy by nominal GDP."),
    (123, "The Nile River is the longest river in the world, stretching over 6,650 kilometers."),
    (124, "The Sahara Desert is the largest hot desert in the world, covering over 9 million square kilometers."),
    (125, "The Amazon River is the largest river in the world by volume, with a discharge greater than the next seven largest rivers combined."),
    (126, "The Pacific Ocean is the largest ocean in the world, covering over 60 million square miles."),
    (127, "The Indian Ocean is the third largest ocean in the world, covering approximately 20% of the Earth's surface."),
    (128, "The Arctic Ocean is the smallest and shallowest of the world's five major oceans."),
    (129, "The largest country in the world by land area is Russia, covering over 17 million square kilometers."),
    (130, "The smallest country in the world by land area is Vatican City, covering just 44 hectares."),
    (131, "The largest mammal in the world is the blue whale, which can grow up to 100 feet long and weigh over 200 tons."),
    (132, "The fastest land animal in the world is the cheetah, which can run at speeds up to 75 miles per hour."),
    (133, "The African elephant is the largest land animal in the world, weighing up to 14,000 pounds."),
    (134, "The giraffe is the tallest land animal in the world, with males reaching up to 18 feet tall."),
    (135, "The most venomous animal in the world is the box jellyfish, which can cause death in just a few minutes."),
    (136, "The largest bird in the world by wingspan is the wandering albatross, with a wingspan of up to 12 feet."),
    (137, "The ostrich is the largest bird in the world by weight, weighing up to 350 pounds."),
    (138, "The hummingbird is the smallest bird in the world, weighing only a few grams."),
    (139, "The Sun is a star located at the center of the Solar System."),
    (140, "The Earth is the third planet from the Sun, and is the only known planet to support life."),
    (141, "The Milky Way is a barred spiral galaxy that contains over 100 billion stars."),
    (142, "The universe is estimated to be approximately 13.8 billion years old."),
    (143, "The speed of light is approximately 299,792,458 meters per second."),
    (144, "The smallest particle in the universe is the quark, which makes up protons and neutrons."),
    (145, "The Higgs boson is a subatomic particle that is responsible for giving other particles mass."),
    (146, "The Big Bang theory is the most widely accepted explanation for the origins of the universe."),
    (147, "Gravity is a fundamental force that governs the motion of objects in the universe."),
    (148, "The Earth is the third planet from the sun and the only known planet to support life."),
    (149, "The sun is a star located at the center of the solar system."),
    (150, "A black hole is a region of space with gravitational forces so strong that nothing can escape."),
    (151, "Astronomy is the study of celestial objects and phenomena outside of the Earth's atmosphere."),
    (152, "The International Space Station is a habitable artificial satellite in low Earth orbit."),
    (153, "The Apollo 11 mission was the first crewed mission to land on the moon."),
    (154, "The Kuiper Belt is a region of the solar system beyond the orbit of Neptune that contains many small icy bodies."),
    (155, "Dark matter is a hypothetical form of matter that is thought to make up approximately 85% of the matter in the universe."),
    (156, "The Oort Cloud is a hypothetical cloud of icy objects that is thought to surround the solar system."),
    (157, "A light-year is the distance that light travels in one year, approximately 5.88 trillion miles."),
    (158, "The redshift of light from distant galaxies is evidence for the expansion of the universe."),
    (159, "The Doppler effect is the change in frequency of a wave as the source or observer moves relative to each other."),
    (160, "The Planck constant is a fundamental constant that relates the energy of a photon to its frequency."),
    (161, "Astrophysics is the branch of astronomy that deals with the physics of celestial objects."),
    (162, "The speed of sound in air is approximately 343 meters per second at room temperature."),
    (163, "The Earth's magnetic field is generated by the motion of molten iron in the Earth's outer core."),
    (164, "The aurora borealis and aurora australis are natural light displays in the polar regions caused by the interaction of charged particles with the Earth's magnetic field."),
    (165, "The asteroid belt is a region of the solar system between the orbits of Mars and Jupiter that contains many small rocky bodies."),
    (166, "The Tunguska event was a powerful explosion that occurred in Siberia in 1908 and is thought to have been caused by the impact of a meteoroid."),
    (167, "The Chicxulub crater is an impact crater in Mexico that is thought to be the result of the asteroid impact that caused the extinction of the dinosaurs."),
    (168, "The Drake equation is an equation used to estimate the number of intelligent civilizations in the Milky Way galaxy."),
    (169, "The Voyager 1 spacecraft is the most distant human-made object from Earth, currently in interstellar space."),
    (170, "The James Webb Space Telescope is a space telescope set to launch in 2021 that will study the universe in infrared wavelengths."),
    (171, "The Event Horizon Telescope is a network of telescopes that was used to capture the first image of a black hole in 2019."),
    (172, "The Kepler Space Telescope was a space telescope that discovered thousands of exoplanets orbiting other stars."),
    (173, "The Hubble Space Telescope is a space telescope that has made many important discoveries in astronomy and astrophysics."),
    (174, "The cosmic microwave background radiation is a faint glow of electromagnetic radiation left over from the Big Bang."),
    (175, "The Great Barrier Reef is the largest coral reef system in the world, located in Australia's Coral Sea."),
    (176, "The Amazon Rainforest is the largest rainforest in the world, spanning over nine countries in South America."),
    (177, "The Sahara Desert is the largest hot desert in the world, covering most of North Africa."),
    (178, "Mount Everest is the highest peak in the world, located in the Himalayas on the border of Nepal and Tibet."),
    (179, "The Grand Canyon is a steep-sided canyon carved by the Colorado River in Arizona, United States."),
    (180, "The Great Wall of China is the longest wall in the world, stretching over 13,000 miles."),
    (181, "The Statue of Liberty is a colossal neoclassical sculpture on Liberty Island in New York Harbor in the United States."),
    (182, "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France."),
    (183, "The Pyramids of Giza are ancient Egyptian pyramids located in the Giza pyramid complex in Egypt."),
    (184, "The Colosseum is an oval amphitheatre in the centre of Rome, Italy, built of concrete and sand."),
    (185, "The Taj Mahal is an ivory-white marble mausoleum on the right bank of the Yamuna river in the Indian city of Agra."),
    (186, "The Sydney Opera House is a multi-venue performing arts centre in Sydney, New South Wales, Australia."),
    (187, "The Louvre is the world's largest art museum and a historic monument in Paris, France."),
    (188, "The Sistine Chapel is a chapel in the Apostolic Palace, the official residence of the Pope, in Vatican City."),
    (189, "The Kremlin is a fortified complex at the heart of Moscow, Russia, overlooking the Moskva River."),
    (190, "The Tower of London is a historic castle on the north bank of the River Thames in central London, England."),
    (191, "The Golden Gate Bridge is a suspension bridge spanning the Golden Gate, the one-mile-wide strait connecting San Francisco Bay and the Pacific Ocean."),
    (192, "The Angkor Wat is a temple complex in Cambodia and the largest religious monument in the world."),
    (193, "The Machu Picchu is a 15th-century Inca citadel located in the Cusco Region of Peru."),
    (194, "The Neuschwanstein Castle is a 19th-century Romanesque Revival palace on a rugged hill above the village of Hohenschwangau near Füssen in southwest Bavaria, Germany."),
    (195, "The Hagia Sophia is a former Greek Orthodox Christian patriarchal cathedral, later an Ottoman imperial mosque, and now a museum in Istanbul, Turkey."),
    (196, "The Burj Khalifa is a skyscraper in Dubai, United Arab Emirates, and the tallest building in the world."),
    (197, "The Acropolis of Athens is an ancient citadel located on a rocky outcrop above the city of Athens and contains the remains of several ancient buildings."),
    (198, "The Petra is a historic and archaeological city in southern Jordan, famous for its rock-cut architecture."),
    (199, "The Christ the Redeemer is an Art Deco statue of Jesus Christ in Rio de Janeiro, Brazil."),
    (200, "The Mount Fuji is the highest mountain in Japan, located on Honshū, and is an active stratovolcano that last erupted in 1707–08."),
    (201, "The Great Barrier Reef is the world's largest coral reef system, located off the coast of Australia."),
    (202, "The Grand Canyon is a steep-sided canyon carved by the Colorado River in Arizona."),
    (203, "The Amazon River is the largest river in the world by volume, located in South America."),
    (204, "Mount Everest is the highest mountain in the world, located in the Himalayas."),
    (205, "The Sahara Desert is the largest hot desert in the world, located in North Africa."),
    (206, "The Nile River is the longest river in the world, flowing through several African countries."),
    (207, "The Eiffel Tower is a famous landmark in Paris, France, and is one of the most recognizable structures in the world."),
    (208, "The Statue of Liberty is a symbol of freedom and democracy, located on Liberty Island in New York Harbor."),
    (209, "The Great Wall of China is a series of fortifications built along the northern borders of China to protect against invaders."),
    (210, "The Colosseum is an ancient amphitheater in Rome, Italy, and is one of the most famous landmarks in the city."),
    (211, "The Taj Mahal is a white marble mausoleum in Agra, India, and is considered one of the most beautiful buildings in the world."),
    (212, "The Sydney Opera House is a multi-venue performing arts center in Sydney, Australia, and is known for its distinctive design."),
    (213, "The Golden Gate Bridge is a suspension bridge in San Francisco, California, and is one of the most photographed landmarks in the world."),
    (214, "The Kremlin is a historic fortified complex in Moscow, Russia, and serves as the official residence of the President of the Russian Federation."),
    (215, "The Tower Bridge is a combined bascule and suspension bridge in London, England, and is an iconic symbol of the city."),
    (216, "The Burj Khalifa is the tallest building in the world, located in Dubai, United Arab Emirates."),
    (217, "The Great Sphinx of Giza is a large statue of a sphinx located in Egypt, and is believed to have been built during the reign of the Pharaoh Khafre."),
    (218, "The Acropolis is an ancient citadel located on a rocky outcrop above the city of Athens, Greece, and contains several historic buildings."),
    (219, "The Angel Falls is the world's highest uninterrupted waterfall, located in Venezuela."),
    (220, "The Machu Picchu is an ancient Incan citadel located in the Andes Mountains of Peru, and is considered one of the most important archaeological sites in the world."),
    (221, "The Great Barrier Reef is the world's largest coral reef system, located in Australia's Coral Sea."),
    (222, "The Amazon rainforest is the largest tropical rainforest in the world, covering over 7 million square kilometers."),
    (223, "The Sahara is the largest hot desert in the world, covering most of North Africa."),
    (224, "The Himalayas are the highest mountain range in the world, with Mount Everest as its highest peak."),
    (225, "The Grand Canyon is a steep-sided canyon carved by the Colorado River in Arizona, United States."),
    (226, "The Great Wall of China is a series of fortifications built along the northern borders of China to protect against invasions."),
    (227, "The Sphinx is a statue of a mythical creature with the body of a lion and the head of a human, located in Giza, Egypt."),
    (228, "The Eiffel Tower is a wrought iron lattice tower located in Paris, France, and is one of the most recognizable structures in the world."),
    (229, "The Statue of Liberty is a colossal neoclassical sculpture located on Liberty Island in New York Harbor."),
    (230, "The Taj Mahal is a white marble mausoleum located in Agra, India, and is widely regarded as one of the world's most beautiful buildings.")
]   

def create_table():
    connection = sqlite3.connect('AIDB.db')
    cursor = connection.cursor()

    # Create a sample table
    cursor.execute("""
    CREATE TABLE base_table (
        id INTEGER PRIMARY KEY,
        sentence TEXT
    )
    """)

    # Create a sample table
    cursor.execute("""
    CREATE TABLE mapping_table (
        id INTEGER PRIMARY KEY,
        base_id INTEGER,
        word TEXT,
        entity TEXT
    )
    """)


    cursor.execute("""
    CREATE TABLE sample_mapping_table (
        id INTEGER PRIMARY KEY,
        base_id INTEGER,
        word TEXT,
        entity TEXT
    )
    """)


    # Commit the changes
    connection.commit()



def insert_base_table():
    connection = sqlite3.connect('AIDB.db')
    cursor = connection.cursor()

    cursor.executemany("""
    INSERT INTO base_table (id, sentence) VALUES (?, ?)
    """, data)

    # Commit the changes
    connection.commit()

    return


def insert_mapping_table(base_id):
    connection = sqlite3.connect('AIDB.db')
    cursor = connection.cursor()

    # Insert sample data
    base_id = int(base_id)
    entity = model(data[base_id-1][0], data[base_id-1][1])


    cursor.executemany("""
    INSERT INTO mapping_table (base_id, word, entity) VALUES (?, ?, ?)
    """, entity)

    # Commit the changes
    connection.commit()

    return


def insert_sample_mapping_table(base_id):
    connection = sqlite3.connect('AIDB.db')
    cursor = connection.cursor()

    # Insert sample data
    base_id = int(base_id)
    entity = model(data[base_id-1][0], data[base_id-1][1])


    cursor.executemany("""
    INSERT INTO sample_mapping_table (base_id, word, entity) VALUES (?, ?, ?)
    """, entity)

    # Commit the changes
    connection.commit()

    return


def run_accurate_query(cursor):
    connection = sqlite3.connect('AIDB.db')
    cursor = connection.cursor()
    accruate_query = "SELECT COUNT(*) FROM mapping_table"
    accurate_start_time = time.perf_counter()
    accurate_result = simple_query_engine(accruate_query, cursor)
    accurate_end_time = time.perf_counter()
    accurate_query_time = accurate_end_time - accurate_start_time
    return accurate_query_time

def run_approximate_query(cursor):
    approximate_query = "SELECT COUNT(*) FROM sample_mapping_table"
    approximate_start_time = time.perf_counter()
    approximate_result = simple_query_engine(approximate_query, cursor)
    approximate_end_time = time.perf_counter()
    approximate_query_time = approximate_end_time - approximate_start_time
    return approximate_query_time



def main():
    sample_size = 40
    connection = sqlite3.connect('AIDB.db')
    cursor = connection.cursor()

    # ------------------------------- create table -----------------------------------
    create_table()

    # # ## generating rows
    create_start_time = time.perf_counter()
    for i, _ in enumerate(data): 
        insert_mapping_table(i)

    ## get random number
    numbers = list(range(1, len(data)))
    random.shuffle(numbers)
    selected_numbers = numbers[:sample_size]
    ## generate ramdonly sampled mapping table
    for i in selected_numbers:
        insert_sample_mapping_table(i)
    
    create_end_time = time.perf_counter()
    create_time = -create_start_time + create_end_time
    print(f"Create time: {create_time:.8f} seconds")

    # ------------------------------ Compute Accuracy ------------------------------------------
    
    query1 =  "SELECT * FROM mapping_table"
    query2 = "SELECT id, base_id, word, entity FROM mapping_table WHERE word like 'G%' "  
    query3 = "SELECT id, base_id, word, entity FROM mapping_table WHERE base_id = 3 " 
    accruate_query = "SELECT COUNT(*) FROM mapping_table"
    approximate_query = "SELECT COUNT(*) FROM sample_mapping_table"


    ### Get result of accruate query which counts the number of name entities
    accurate_start_time = time.perf_counter()
    accurate_result = simple_query_engine(accruate_query, cursor)
    accurate_end_time = time.perf_counter()

    accurate_query_time = accurate_end_time - accurate_start_time

    print("Results for accurate count:")
    accurate_result = accurate_result[0][0]
    print(accurate_result)
    print(f"Accurate Query time: {accurate_query_time:.8f} seconds")


    # Get result of approximate query which counts the number of name entities
    approximate_start_time = time.perf_counter()
    approximate_result = simple_query_engine(approximate_query, cursor)
    approximate_end_time = time.perf_counter()

    approximate_query_time = approximate_end_time - approximate_start_time

    print(f"Results for approximate count with sample size {sample_size}: ")
    result = approximate_result[0][0]
    result = int( result * len(data) / sample_size)
    print(int(result))
    print(f"Accruarcy: {result/accurate_result}")
    print(f"Approximate Query time: {approximate_query_time:.8f} seconds")


    ## -------------------------------- Draw Graph -------------------------------------
    query_round = 40

    accurate_query_times = []
    approximate_query_times = []
    
    ######## Run accurate query
    for _ in range(query_round):
        start_time = time.perf_counter()
        run_accurate_query(cursor)
        end_time = time.perf_counter()
        query_time = end_time - start_time
        accurate_query_times.append(query_time)

    # Run approximate query
    # for _ in range(query_round):
    #     start_time = time.perf_counter()
    #     run_approximate_query(cursor)
    #     end_time = time.perf_counter()
    #     query_time = end_time - start_time
    #     approximate_query_times.append(query_time)


    accurate_avg_time = sum(accurate_query_times) / len(accurate_query_times)
    # approximate_avg_time = sum(approximate_query_times) / len(approximate_query_times)

    print(f"Average time for accurate query: {accurate_avg_time:.8f} seconds")
    # print(f"Average time for approximate query: {approximate_avg_time:.8f} seconds")

    # ### Plot the results
    plt.plot(accurate_query_times, label="Accurate Query")
    # plt.plot(approximate_query_times, label="Approximate Query")
    plt.xlabel("Round")
    plt.ylabel("Time (seconds)")
    plt.title("Accurate vs Approximate Query Times")
    plt.legend()
    plt.show()

    

if __name__ == "__main__":
    main()

