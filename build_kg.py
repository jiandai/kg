import rdflib
from rdflib import Graph, Literal, RDF, RDFS, URIRef, Namespace
from rdflib.namespace import FOAF, XSD

# Initialize Graph
g = Graph()

# Define Namespace
EX = Namespace("http://example.org/solar_system/")
g.bind("ex", EX)

# Define Classes
CelestialBody = EX.CelestialBody
Star = EX.Star
Planet = EX.Planet
DwarfPlanet = EX.DwarfPlanet
System = EX.System

# Function to clean and create URI
def create_uri(name):
    return EX[name.replace(" ", "_")]

# Add basic ontology structure (optional but good for validation)
g.add((Star, RDF.type, RDFS.Class))
g.add((Star, RDFS.subClassOf, CelestialBody))
g.add((Planet, RDF.type, RDFS.Class))
g.add((Planet, RDFS.subClassOf, CelestialBody))
g.add((DwarfPlanet, RDF.type, RDFS.Class))
g.add((DwarfPlanet, RDFS.subClassOf, CelestialBody))

def build_kg(file_path):
    print(f"Reading {file_path}...")
    with open(file_path, 'r') as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Simple rule-based extraction
        if "Sun" in line and "center of the Solar System" in line:
            sun = create_uri("Sun")
            solar_system = create_uri("Solar_System")
            g.add((sun, RDF.type, Star))
            g.add((sun, EX.isCenterOf, solar_system))
            g.add((solar_system, RDF.type, System))

        elif "Mercury" in line and "smallest planet" in line:
            mercury = create_uri("Mercury")
            g.add((mercury, RDF.type, Planet))
            g.add((mercury, EX.hasAttribute, Literal("smallest")))
            g.add((mercury, EX.orbits, create_uri("Sun"))) # Implicit knowledge

        elif "Venus" in line and "second planet" in line:
            venus = create_uri("Venus")
            g.add((venus, RDF.type, Planet))
            g.add((venus, EX.orderFromSun, Literal(2, datatype=XSD.integer)))
            g.add((venus, EX.orbits, create_uri("Sun")))

        elif "Mars" in line and "Red Planet" in line:
            mars = create_uri("Mars")
            g.add((mars, RDF.type, Planet))
            g.add((mars, EX.hasNickname, Literal("Red Planet")))
            g.add((mars, EX.orbits, create_uri("Sun")))

        elif "Jupiter" in line and "largest planet" in line:
            jupiter = create_uri("Jupiter")
            g.add((jupiter, RDF.type, Planet))
            g.add((jupiter, EX.hasAttribute, Literal("largest")))
            g.add((jupiter, EX.orbits, create_uri("Sun")))

        elif "Saturn" in line and "ring system" in line:
            saturn = create_uri("Saturn")
            g.add((saturn, RDF.type, Planet))
            g.add((saturn, EX.hasFeature, Literal("ring system")))
            g.add((saturn, EX.orbits, create_uri("Sun")))

        elif "Uranus" in line and "ice giant" in line:
            uranus = create_uri("Uranus")
            g.add((uranus, RDF.type, Planet))
            g.add((uranus, EX.classification, Literal("ice giant")))
            g.add((uranus, EX.orbits, create_uri("Sun")))

        elif "Neptune" in line and "farthest known planet" in line:
            neptune = create_uri("Neptune")
            g.add((neptune, RDF.type, Planet))
            g.add((neptune, EX.hasAttribute, Literal("farthest known")))
            g.add((neptune, EX.orbits, create_uri("Sun")))

        elif "Pluto" in line and "dwarf planet" in line:
            pluto = create_uri("Pluto")
            g.add((pluto, RDF.type, DwarfPlanet))
            g.add((pluto, EX.orbits, create_uri("Sun")))

    # Serialize
    output_file = "solar_system.ttl"
    g.serialize(destination=output_file, format="turtle")
    print(f"Knowledge Graph saved to {output_file}")

    # Verify
    print("\n--- Verification: All Planets ---")
    query = """
    SELECT ?planet ?type
    WHERE {
        ?planet a ?type .
        FILTER (?type = ex:Planet || ?type = ex:DwarfPlanet)
    }
    """
    for row in g.query(query):
        print(f"{row.planet} is a {row.type}")

if __name__ == "__main__":
    build_kg("solar_system.txt")
