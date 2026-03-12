// Coastal Ecosystem Features — Keta Lagoon Complex & Songor Ramsar Sites
// Representative coastal ecosystem data points and polygons

const coastalPoints = [
    // === Keta Lagoon Complex ===
    { name: 'Keta Seagrass Bed 1', desc: 'Dense Halodule uninervis seagrass meadow near Keta beach', lat: 5.9083, lng: 1.0050, ecosystem_type: 'seagrass', site: 'Keta' },
    { name: 'Keta Seagrass Bed 2', desc: 'Mixed seagrass bed (Halodule/Thalassia) at lagoon mouth', lat: 5.8992, lng: 1.0120, ecosystem_type: 'seagrass', site: 'Keta' },
    { name: 'Dzita Saltmarsh', desc: 'Spartina saltmarsh fringe along Dzita coastline', lat: 5.7740, lng: 0.7819, ecosystem_type: 'saltmarsh', site: 'Keta' },
    { name: 'Woe Tidal Flat', desc: 'Exposed tidal mudflats with shorebird foraging habitat', lat: 5.8336, lng: 0.9537, ecosystem_type: 'tidal flat', site: 'Keta' },
    { name: 'Anloga Coastal Vegetation', desc: 'Coastal scrub and herbaceous vegetation on sandy substrate', lat: 5.7972, lng: 0.7312, ecosystem_type: 'coastal vegetation', site: 'Keta' },
    { name: 'Keta Beach Wrack Zone', desc: 'High tide wrack line with organic matter accumulation', lat: 5.9150, lng: 1.0200, ecosystem_type: 'beach', site: 'Keta' },
    { name: 'Anyanui Tidal Channel', desc: 'Active tidal channel connecting lagoon to sea, nursery habitat', lat: 5.7835, lng: 0.7213, ecosystem_type: 'tidal channel', site: 'Keta' },
    { name: 'Agbledome Mudflat', desc: 'Intertidal mudflat with invertebrate communities', lat: 5.7866, lng: 0.7539, ecosystem_type: 'tidal flat', site: 'Keta' },
    { name: 'Salo Saltmarsh', desc: 'Fringing saltmarsh along Salo lagoon edge', lat: 5.8244, lng: 0.7992, ecosystem_type: 'saltmarsh', site: 'Keta' },
    { name: 'Keta Lagoon Open Water', desc: 'Open water zone with submerged aquatic vegetation', lat: 5.8500, lng: 0.9800, ecosystem_type: 'open water', site: 'Keta' },
    { name: 'Aborlorvie Coastal Scrub', desc: 'Dense coastal scrub vegetation on barrier island', lat: 6.0260, lng: 0.9306, ecosystem_type: 'coastal vegetation', site: 'Keta' },
    { name: 'Vodza Beach Dune', desc: 'Foredune and backdune coastal dune system', lat: 5.9311, lng: 0.9899, ecosystem_type: 'coastal dune', site: 'Keta' },

    // === Ada/Songor Lagoon ===
    { name: 'Songor Saltflat 1', desc: 'Salt flat with halophytic vegetation, migratory bird staging area', lat: 5.8386, lng: 0.6519, ecosystem_type: 'salt flat', site: 'Ada/Songor' },
    { name: 'Songor Saltflat 2', desc: 'Extensive salt pan complex, artisanal salt harvesting area', lat: 5.8472, lng: 0.6350, ecosystem_type: 'salt flat', site: 'Ada/Songor' },
    { name: 'Ada Bar Seagrass', desc: 'Seagrass meadow at Volta River mouth, Ada Foah', lat: 5.7894, lng: 0.6133, ecosystem_type: 'seagrass', site: 'Ada/Songor' },
    { name: 'Big Ada Tidal Flat', desc: 'Extensive tidal mudflat, important shorebird habitat', lat: 5.8071, lng: 0.6082, ecosystem_type: 'tidal flat', site: 'Ada/Songor' },
    { name: 'Wasa Kuse Saltmarsh', desc: 'Saltmarsh fringe with Avicennia transition zone', lat: 5.8386, lng: 0.5552, ecosystem_type: 'saltmarsh', site: 'Ada/Songor' },
    { name: 'Azizanya Tidal Channel', desc: 'Branching tidal creek with high biodiversity', lat: 5.7709, lng: 0.6531, ecosystem_type: 'tidal channel', site: 'Ada/Songor' },
    { name: 'Togbloku Coastal Lagoon', desc: 'Shallow coastal lagoon with macroalgae and submerged plants', lat: 5.8387, lng: 0.5539, ecosystem_type: 'coastal lagoon', site: 'Ada/Songor' },
    { name: 'Obane Creek Mouth', desc: 'Creek mouth with estuarine coastal vegetation transition', lat: 5.8049, lng: 0.4233, ecosystem_type: 'estuary', site: 'Ada/Songor' },
    { name: 'Patukope Beach Dune', desc: 'Coastal sand dune system with pioneer vegetation', lat: 5.7852, lng: 0.5702, ecosystem_type: 'coastal dune', site: 'Ada/Songor' },
    { name: 'Songor Open Water Zone', desc: 'Open water area with floating macrophytes', lat: 5.8550, lng: 0.6250, ecosystem_type: 'open water', site: 'Ada/Songor' }
];

const coastalPolygons = [
    {
        name: 'Keta Lagoon Core Zone',
        desc: 'Core conservation zone of the Keta Lagoon Complex Ramsar Site. Supports critical waterbird breeding and migratory habitat.',
        ecosystem_type: 'ramsar core zone',
        site: 'Keta',
        geojson: {
            type: "Feature",
            properties: { name: "Keta Lagoon Core Zone" },
            geometry: {
                type: "Polygon",
                coordinates: [[
                    [0.7000, 5.7800], [0.7800, 5.7800], [0.9000, 5.8000],
                    [1.0000, 5.8500], [1.0200, 5.9000], [0.9500, 5.9200],
                    [0.8000, 5.9000], [0.7000, 5.8600], [0.6800, 5.8200],
                    [0.7000, 5.7800]
                ]]
            }
        }
    },
    {
        name: 'Songor Lagoon Wetland Zone',
        desc: 'Internationally important wetland zone of the Songor Lagoon, including salt flats, tidal channels and fringing habitats.',
        ecosystem_type: 'ramsar core zone',
        site: 'Ada/Songor',
        geojson: {
            type: "Feature",
            properties: { name: "Songor Lagoon Wetland Zone" },
            geometry: {
                type: "Polygon",
                coordinates: [[
                    [0.5300, 5.8100], [0.5800, 5.8100], [0.6500, 5.8200],
                    [0.6800, 5.8500], [0.6700, 5.8700], [0.6200, 5.8800],
                    [0.5600, 5.8700], [0.5200, 5.8500], [0.5100, 5.8300],
                    [0.5300, 5.8100]
                ]]
            }
        }
    },
    {
        name: 'Keta Barrier Beach Dune System',
        desc: 'Linear barrier beach and sand dune system along the Keta coastline. Provides coastal protection and nesting habitat.',
        ecosystem_type: 'coastal dune',
        site: 'Keta',
        geojson: {
            type: "Feature",
            properties: { name: "Keta Barrier Beach" },
            geometry: {
                type: "Polygon",
                coordinates: [[
                    [0.7100, 5.7700], [1.0300, 5.7700], [1.0350, 5.7800],
                    [0.7100, 5.7800], [0.7100, 5.7700]
                ]]
            }
        }
    }
];
