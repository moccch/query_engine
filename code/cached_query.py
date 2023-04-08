import sqlite3
import re
import time
from two_models import ner_model, summarizer_model

text_data = [
    (0, """The World Health Organization (WHO) is a specialized agency of the United Nations that is responsible for international 
         public health. It was established in 1948 and is headquartered in Geneva, Switzerland. The WHO is responsible for 
         coordinating and supporting efforts to improve public health around the world, including efforts to combat infectious 
         diseases, promote healthy lifestyles, and provide access to essential medicines and vaccines."""),
    (1, """Apple Inc. is an American multinational technology company headquartered in Cupertino, California, that designs, 
        develops, and sells consumer electronics, computer software, and online services. It is considered one of the Big Five companies 
        in the U.S. information technology industry, along with Amazon, Google, Microsoft, and Facebook. The company's hardware products
        include the iPhone smartphone, the iPad tablet computer, the Mac personal computer, the iPod portable media player, the Apple 
        Watch smartwatch, the Apple TV digital media player, the AirPods wireless earbuds, and the HomePod smart speaker."""),
    (2, """The history of Apple Inc. dates back to 1976 when it was founded by Steve Jobs, Steve Wozniak, and Ronald Wayne. The 
        company started out by developing and selling personal computers and later expanded into consumer electronics and software 
        development. In 2007, Apple introduced the iPhone, which revolutionized the smartphone industry. Today, Apple is one of the 
        most valuable companies in the world with a market capitalization of over $2 trillion."""),
    (3, """Amazon.com, Inc. is an American multinational technology company based in Seattle, Washington, which focuses on e-commerce, 
        cloud computing, digital streaming, and artificial intelligence. It is one of the Big Five companies in the U.S. information 
        technology industry, along with Apple, Google, Microsoft, and Facebook. Amazon is known for its disruption of well-established 
        industries through technological innovation and mass scale. It is the world's largest online marketplace, AI assistant 
        provider, and cloud computing platform as measured by revenue and market capitalization."""),
    (4, """Microsoft Corporation is an American multinational technology company based in Redmond, Washington, that develops, 
        licenses, and sells computer software, consumer electronics, and personal computers. It is one of the Big Five companies in 
        the U.S. information technology industry, along with Apple, Google, Amazon, and Facebook. Microsoft is best known for its 
        Windows operating system and the Microsoft Office suite of productivity software."""),
    (5, """Google LLC is an American multinational technology company that specializes in Internet-related services and products, 
        which include online advertising technologies, a search engine, cloud computing, software, and hardware. It is one of the Big 
        Five companies in the U.S. information technology industry, along with Apple, Amazon, Microsoft, and Facebook. Google was 
        founded in 1998 by Larry Page and Sergey Brin while they were Ph.D. students at Stanford University."""),
    (6, """Facebook, Inc. is an American social media and technology company based in Menlo Park, California. It was founded by Mark 
        Zuckerberg, along with fellow Harvard College students and roommates, in 2004. Facebook is one of the Big Five companies in 
        the U.S. information technology industry, along with Apple, Amazon, Google, and Microsoft. It is the world's largest social 
        network, with over 2.8 billion monthly active users as of December 2020."""),
    (7, """Tesla, Inc. is an American electric vehicle and clean energy company based in Palo Alto, California. It was founded in 
        2003 by Elon Musk, Martin Eberhard, Marc Tarpenning, JB Straubel, and Ian Wright. Tesla designs and manufactures electric 
        cars, battery energy storage, and solar panels. The company is known for its innovative approach to sustainable energy 
        solutions and is one of the world's"""),
    (8, """Netflix, Inc. is an American subscription-based streaming service that offers movies, TV shows, and documentaries. It was
        founded in 1997 by Reed Hastings and Marc Randolph in Scotts Valley, California. Netflix is one of the world's leading
        entertainment companies and has over 200 million subscribers in more than 190 countries. The company is known for its
        original content, which includes critically acclaimed shows like "Stranger Things," "The Crown," and "Narcos."""),
    (9, """The Walt Disney Company is an American media and entertainment conglomerate that was founded in 1923 by Walt Disney and
        Roy O. Disney. The company is known for its theme parks, movies, TV shows, and merchandise. Disney is one of the world's
        largest media companies, with assets that include ABC, ESPN, Pixar, Marvel Studios, and Lucasfilm. In 2019, the company
        launched Disney+, its own streaming service, which quickly became one of the most popular services of its kind."""),
    (10, """Twitter, Inc. is an American microblogging and social networking service that was founded in 2006 by Jack Dorsey,
        Biz Stone, and Evan Williams. Twitter allows users to post and interact with messages, known as "tweets," which are limited
        to 280 characters. The platform is known for its role in facilitating public conversations, breaking news, and political
        discourse. Twitter has over 330 million monthly active users and is one of the most popular social media platforms in the
        world."""),
    (11, """Alphabet Inc. is an American multinational conglomerate that owns Google and several other companies. It was created in 
         2015 as a restructuring of Google and became the parent company of Google and several former Google subsidiaries. Alphabet 
         is one of the Big Five companies in the U.S. information technology industry, along with Apple, Amazon, Microsoft, and 
         Facebook. Alphabet's subsidiaries include Google, YouTube, Waymo, and several others."""),
    (12, """IBM (International Business Machines Corporation) is an American multinational technology company that produces and 
         sells computer hardware, middleware, and software. It is one of the oldest technology companies in the world, with a history 
         that dates back to 1911. IBM is known for its mainframe computers, which are used by large organizations and governments 
         around the world. The company is also a major player in the cloud computing and artificial intelligence industries."""),
    (13, """Intel Corporation is an American multinational technology company that produces computer processors and other 
         semiconductor components. It was founded in 1968 and is headquartered in Santa Clara, California. Intel is one of the largest 
         semiconductor manufacturers in the world and is known for its x86 architecture, which is used in most personal computers. The 
         company also produces processors for servers, mobile devices, and other electronics."""),
    (14, """Samsung Electronics Co., Ltd. is a South Korean multinational electronics company that produces a wide range of 
         electronics and appliances. It was founded in 1969 and is headquartered in Seoul, South Korea. Samsung is one of the largest 
         technology companies in the world and is known for its smartphones, televisions, and memory chips. The company also produces 
         home appliances, such as refrigerators and washing machines."""),
    (15, """Sony Corporation is a Japanese multinational conglomerate that produces electronics, gaming, entertainment, and financial 
         services. It was founded in 1946 and is headquartered in Tokyo, Japan. Sony is known for its PlayStation gaming consoles, 
         Xperia smartphones, and a wide range of consumer electronics, including televisions, cameras, and audio equipment. The 
         company also has a large presence in the entertainment industry through its music, movie, and television divisions."""),
    (16, """The Coca-Cola Company is an American multinational beverage corporation that produces and sells carbonated soft drinks, 
         juices, and other non-alcoholic beverages. It was founded in 1886 and is headquartered in Atlanta, Georgia. Coca-Cola is one 
         of the most recognizable brands in the world, and its flagship product, Coca-Cola, is the world's best-selling soft drink."""),
    (17, """Pfizer Inc. is an American multinational pharmaceutical corporation that develops and produces medicines and vaccines 
         for a wide range of medical conditions. It was founded in 1849 and is headquartered in New York City. Pfizer is one of the 
         world's largest pharmaceutical companies and is known for developing a wide range of products, including Viagra, Lipitor, 
         and Celebrex."""),
    (18, """General Electric Company (GE) is an American multinational conglomerate that produces a wide range of products and 
         services, including aircraft engines, power generation, and healthcare equipment. It was founded in 1892 and is 
         headquartered in Boston, Massachusetts. GE is one of the largest companies in the world and has a presence in many different 
         industries, including aviation, energy, and healthcare."""),
    (19, """The Procter & Gamble Company (P&G) is an American multinational consumer goods corporation that produces a wide range of 
         household and personal care products. It was founded in 1837 and is headquartered in Cincinnati, Ohio. P&G is one of the 
         largest consumer goods companies in the world and is known for brands such as Tide, Crest, Gillette, and Pampers."""),
    (20, """The Boeing Company is an American multinational corporation that designs, manufactures, and sells airplanes, rockets, 
         satellites, and missiles. It was founded in 1916 and is headquartered in Chicago, Illinois. Boeing is one of the largest 
         aerospace companies in the world and is known for products such as the 747, 777, and 787 aircraft."""),
    (21, """The Goldman Sachs Group, Inc. is an American multinational investment bank and financial services company that offers a 
         wide range of financial services to corporations, governments, and individuals. It was founded in 1869 and is 
         headquartered in New York City. Goldman Sachs is one of the largest investment banks in the world and is known for its 
         involvement in mergers and acquisitions, initial public offerings (IPOs), and other financial transactions."""),
    (22, """The Walt Disney Company is an American media and entertainment conglomerate that was founded in 1923 by Walt Disney and 
         Roy O. Disney. The company is known for its theme parks, movies, TV shows, and merchandise. Disney is one of the world's 
         largest media companies, with assets that include ABC, ESPN, Pixar, Marvel Studios, and Lucasfilm. In 2019, the company 
         launched Disney+, its own streaming service, which quickly became one of the most popular services of its kind."""),
    (23, """The Ford Motor Company is an American multinational automaker that designs, manufactures, and sells cars, trucks, and 
         SUVs. It was founded in 1903 by Henry Ford and is headquartered in Dearborn, Michigan. Ford is one of the largest 
         automakers in the world and is known for its iconic Mustang and F-150 vehicles."""),
    (24, """The Home Depot, Inc. is an American home improvement retailer that sells a wide range of building materials, tools, and 
         other home improvement products. It was founded in 1978 and is headquartered in Atlanta, Georgia. The Home Depot is one of 
         the largest home improvement retailers in the world, with over 2,200 stores in North America."""),
    (25, """The Coca-Cola Company is an American multinational beverage corporation that produces and sells carbonated soft drinks, 
         juices, and other non-alcoholic beverages. It was founded in 1886 and is headquartered in Atlanta, Georgia. Coca-Cola is one 
         of the most recognizable brands in the world, and its flagship product, Coca-Cola, is the world's best-selling soft drink."""),
    (26, """The New York Times is an American daily newspaper that has been published since 1851. It is one of the largest and most 
         prestigious newspapers in the world, with a reputation for in-depth reporting and investigative journalism. The New York 
         Times covers a wide range of topics, including politics, business, culture, science, and technology."""),
    (27, """CNN (Cable News Network) is an American news-based cable television channel that was founded in 1980. It is one of the 
         largest and most widely watched news networks in the world, with a reputation for breaking news and live coverage of major 
         events. CNN covers a wide range of topics, including politics, business, sports, entertainment, and international news."""),
    (28, """The University of Oxford is a collegiate research university located in Oxford, England. It is one of the oldest and most 
         prestigious universities in the world, with a history that dates back to the 12th century. Oxford is known for its academic 
         excellence and research achievements in a wide range of disciplines, including science, humanities, and social sciences."""),
    (29, """The United Nations (UN) is an intergovernmental organization that was founded in 1945 to promote international 
         cooperation and peace. It is headquartered in New York City and has 193 member states. The UN is known for its efforts in 
         conflict resolution, disaster relief, and sustainable development, among other issues.""")
]

summary_cached_dic = {}
ner_cached_dic = {}

def create_table():
    connection = sqlite3.connect('newAIDB.db')
    cursor = connection.cursor()

    # Create a sample table
    cursor.execute("""
    CREATE TABLE base_table (
        id INTEGER PRIMARY KEY,
        passage TEXT
    )
    """)

    # Create a table for text summary
    cursor.execute("""
    CREATE TABLE summary_table (
        id INTEGER PRIMARY KEY,
        base_id INTEGER,
        summary TEXT
    )
    """)

    # Create a table for summary NER
    cursor.execute("""
    CREATE TABLE ner_table (
        id INTEGER PRIMARY KEY,
        summary_id INTEGER,
        word TEXT,
        entity TEXT
    )
    """)

    # Commit the changes
    connection.commit()


def insert_base_table():
    connection = sqlite3.connect('newAIDB.db')
    cursor = connection.cursor()
    cursor.executemany("""
    INSERT INTO base_table (id, passage) VALUES (?, ?)
    """, text_data)
    connection.commit()
    return


def insert_summary_table(base_id):
    connection = sqlite3.connect('newAIDB.db')
    cursor = connection.cursor()
    text = summarizer_model(text_data[base_id][0], text_data[base_id][1])
    cursor.executemany("""
    INSERT INTO summary_table (base_id, summary) VALUES (?, ?)
    """, [text])
    summary_cached_dic[base_id] = [(base_id,text[1])]
    connection.commit()
    return

def insert_ner_table(summary_id):
    connection = sqlite3.connect('newAIDB.db')
    cursor = connection.cursor()

    ## check summary_id in summary_table or not
    # if not insert into summary_table first
    if summary_id not in summary_cached_dic:
        insert_summary_table(summary_id)

    ner = ner_model(summary_id, summary_cached_dic[summary_id][0][1])
    cursor.executemany("""
    INSERT INTO ner_table (summary_id, word, entity) VALUES (?, ?, ?)
    """, ner)
    ner_cached_dic[summary_id] = ner
    connection.commit()

    return

def mvp_query_engine(query):
    # Parse the query
    query_parts = query.lower().split()
    select_index = query_parts.index("select")
    from_index = query_parts.index("from")
    where_index = query_parts.index("where") if "where" in query_parts else -1

    # Extract columns, table, and condition
    columns = " ".join(query_parts[select_index + 1:from_index]).split(", ")
    table = query_parts[from_index + 1]
    condition = " ".join(query_parts[where_index + 1:]) if where_index != -1 else None

    equal_match = re.search(r"(\w+)\s*=\s*('([^']+)'|(\d+))", condition)
    column, value = equal_match.group(1), equal_match.group(3) or equal_match.group(4)

    if (table=="ner_table"):
        value = int(value)
        if value in ner_cached_dic:
            return ner_cached_dic[value]
        else:
            insert_ner_table(value)
            return ner_cached_dic[value]

    if (table=="summary_table"):
        value = int(value)
        if value in summary_cached_dic:
            return summary_cached_dic[value]
        else:
            insert_summary_table(value)
            return summary_cached_dic[value]
        
    return []


def main():
    create_table()

    connection = sqlite3.connect('newAIDB.db')
    cursor = connection.cursor()

    ## insert summary
    # insert_ner_table(6)
    # insert_summary_table(6)

    query = "SELECT summary_id, word, entity FROM ner_table WHERE summary_id = 6"
    # query = "SELECT base_id, summary FROM summary_table WHERE base_id = 6"


    print('\n')
    print('--------------------------Optimized query with caching-------------------------')
    optimized_query_start_time = time.perf_counter()
    results = mvp_query_engine(query)
    optimized_query_end_time = time.perf_counter()
    optimized_query_time = optimized_query_end_time - optimized_query_start_time
    print(results)
    print(f"Optimized Query time: {optimized_query_time:.8f} seconds")

    print('--------------------------------Normal query------------------------------------')
    query_start_time = time.perf_counter()
    cursor.execute(query)
    results = cursor.fetchall()
    query_end_time = time.perf_counter()
    query_time = query_end_time - query_start_time
    print(results)
    print(f"Normal Query time: {query_time:.8f} seconds")


if __name__ == "__main__":
    main()
