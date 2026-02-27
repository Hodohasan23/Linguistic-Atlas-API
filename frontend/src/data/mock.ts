export interface Language {
  id: string;
  name: string;
  isoCode: string;
  glottocode: string;
  macroarea: string;
  country: string;
  family: string;
  level: string;
  latitude: number;
  longitude: number;
  speakers: number;
  status: string;
  description: string;
}

export interface LanguageSet {
  id: string;
  title: string;
  description: string;
  tags: string[];
  languageIds: string[];
  createdAt: string;
}

export const MACROAREAS = [
  "Africa",
  "Eurasia",
  "North America",
  "South America",
  "Papunesia",
  "Australia",
] as const;

export const LEVELS = ["language", "family", "dialect", "isolate"] as const;

export const MACROAREA_COLORS: Record<string, string> = {
  Africa: "#d9734c",
  Eurasia: "#5a9e6f",
  "North America": "#3b82c4",
  "South America": "#1ba8b0",
  Papunesia: "#8b5ec4",
  Australia: "#d4953a",
};

export const mockLanguages: Language[] = [
  { id: "1", name: "Mandarin Chinese", isoCode: "cmn", glottocode: "mand1415", macroarea: "Eurasia", country: "China", family: "Sino-Tibetan", level: "language", latitude: 39.9, longitude: 116.4, speakers: 920000000, status: "Safe", description: "The most spoken language in the world by number of native speakers." },
  { id: "2", name: "Yoruba", isoCode: "yor", glottocode: "yoru1245", macroarea: "Africa", country: "Nigeria", family: "Atlantic-Congo", level: "language", latitude: 7.4, longitude: 3.9, speakers: 45000000, status: "Safe", description: "A tonal language spoken in West Africa." },
  { id: "3", name: "Navajo", isoCode: "nav", glottocode: "nava1243", macroarea: "North America", country: "United States", family: "Athabaskan-Eyak-Tlingit", level: "language", latitude: 36.1, longitude: -109.5, speakers: 170000, status: "Vulnerable", description: "An Athabaskan language of the American Southwest." },
  { id: "4", name: "Quechua", isoCode: "que", glottocode: "quec1387", macroarea: "South America", country: "Peru", family: "Quechuan", level: "family", latitude: -13.5, longitude: -71.9, speakers: 8900000, status: "Vulnerable", description: "A language family spoken primarily in the Andes." },
  { id: "5", name: "Tok Pisin", isoCode: "tpi", glottocode: "tokp1240", macroarea: "Papunesia", country: "Papua New Guinea", family: "Creole", level: "language", latitude: -5.4, longitude: 145.8, speakers: 4000000, status: "Safe", description: "An English-based creole widely spoken in Papua New Guinea." },
  { id: "6", name: "Pitjantjatjara", isoCode: "pjt", glottocode: "pitj1243", macroarea: "Australia", country: "Australia", family: "Pama-Nyungan", level: "language", latitude: -26.1, longitude: 129.9, speakers: 3500, status: "Endangered", description: "An Australian Aboriginal language of the Western Desert group." },
  { id: "7", name: "Arabic", isoCode: "ara", glottocode: "arab1395", macroarea: "Eurasia", country: "Saudi Arabia", family: "Afro-Asiatic", level: "language", latitude: 24.7, longitude: 46.7, speakers: 310000000, status: "Safe", description: "A Central Semitic language with global reach." },
  { id: "8", name: "Swahili", isoCode: "swh", glottocode: "swah1253", macroarea: "Africa", country: "Tanzania", family: "Atlantic-Congo", level: "language", latitude: -6.8, longitude: 37.7, speakers: 16000000, status: "Safe", description: "A Bantu language and lingua franca of East Africa." },
  { id: "9", name: "Cherokee", isoCode: "chr", glottocode: "cher1273", macroarea: "North America", country: "United States", family: "Iroquoian", level: "language", latitude: 35.5, longitude: -83.5, speakers: 2100, status: "Severely Endangered", description: "An Iroquoian language with its own unique syllabary." },
  { id: "10", name: "Guaraní", isoCode: "grn", glottocode: "para1311", macroarea: "South America", country: "Paraguay", family: "Tupian", level: "language", latitude: -25.3, longitude: -57.6, speakers: 6500000, status: "Safe", description: "A Tupian language and co-official language of Paraguay." },
  { id: "11", name: "Tagalog", isoCode: "tgl", glottocode: "taga1270", macroarea: "Papunesia", country: "Philippines", family: "Austronesian", level: "language", latitude: 14.6, longitude: 120.9, speakers: 28000000, status: "Safe", description: "An Austronesian language forming the basis of Filipino." },
  { id: "12", name: "Warlpiri", isoCode: "wbp", glottocode: "warl1254", macroarea: "Australia", country: "Australia", family: "Pama-Nyungan", level: "language", latitude: -21.2, longitude: 131.8, speakers: 2500, status: "Endangered", description: "A Pama-Nyungan language of central Australia." },
  { id: "13", name: "Hindi", isoCode: "hin", glottocode: "hind1269", macroarea: "Eurasia", country: "India", family: "Indo-European", level: "language", latitude: 28.6, longitude: 77.2, speakers: 600000000, status: "Safe", description: "An Indo-Aryan language and one of India's official languages." },
  { id: "14", name: "Hausa", isoCode: "hau", glottocode: "haus1257", macroarea: "Africa", country: "Nigeria", family: "Afro-Asiatic", level: "language", latitude: 12.0, longitude: 8.5, speakers: 63000000, status: "Safe", description: "A Chadic language widely spoken across West Africa." },
  { id: "15", name: "Inuktitut", isoCode: "iku", glottocode: "inuk1238", macroarea: "North America", country: "Canada", family: "Eskimo-Aleut", level: "language", latitude: 63.7, longitude: -68.5, speakers: 39000, status: "Vulnerable", description: "An Eskimo-Aleut language spoken in Arctic Canada." },
  { id: "16", name: "Aymara", isoCode: "aym", glottocode: "nucl1667", macroarea: "South America", country: "Bolivia", family: "Aymaran", level: "language", latitude: -16.5, longitude: -68.1, speakers: 1700000, status: "Vulnerable", description: "An Aymaran language spoken in the Andes region." },
  { id: "17", name: "Japanese", isoCode: "jpn", glottocode: "nucl1643", macroarea: "Eurasia", country: "Japan", family: "Japonic", level: "language", latitude: 35.7, longitude: 139.7, speakers: 128000000, status: "Safe", description: "A Japonic language and national language of Japan." },
  { id: "18", name: "Zulu", isoCode: "zul", glottocode: "zulu1248", macroarea: "Africa", country: "South Africa", family: "Atlantic-Congo", level: "language", latitude: -28.8, longitude: 31.1, speakers: 12000000, status: "Safe", description: "A Southern Bantu language with distinctive click consonants." },
];

export const mockLanguageSets: LanguageSet[] = [
  {
    id: "set-1",
    title: "Endangered Languages of Oceania",
    description: "A collection of endangered and vulnerable languages from the Oceania region for comparative study.",
    tags: ["endangered", "oceania", "conservation"],
    languageIds: ["5", "6", "11", "12"],
    createdAt: "2024-01-15",
  },
  {
    id: "set-2",
    title: "Tonal Languages Worldwide",
    description: "Languages that use tone to distinguish meaning, spanning multiple continents and families.",
    tags: ["tonal", "phonology", "typology"],
    languageIds: ["1", "2", "14", "18"],
    createdAt: "2024-02-20",
  },
  {
    id: "set-3",
    title: "Indigenous Americas",
    description: "Indigenous languages of North and South America for cross-regional comparison.",
    tags: ["indigenous", "americas", "revitalization"],
    languageIds: ["3", "4", "9", "10", "15", "16"],
    createdAt: "2024-03-08",
  },
];
