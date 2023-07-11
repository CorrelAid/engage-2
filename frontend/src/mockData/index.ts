export const adminUser = {
  name: "Frie Preu",
  initials: "FP",
};

export const legalForms = [
  "e.V. - Eingetragener Verein",
  "gGmbH - Gemeinnützige Gesellschaft mit beschränkter Haftung",
  "gUG - gemeinnützige Unternehmergesellschaft (haftungsbeschränkt)",
  "Stiftung",
];

export const sectors = [
  "LGBTQ+ organizations",
  "Women's and gender equality organizations",
  "Environmental and conservation organizations",
  "Community development and advocacy groups",
  "Healthcare and social services organizations",
  "Education and youth development organizations",
  "Arts and culture organizations",
  "International and humanitarian aid organizations",
  "Religious and faith-based organizations",
  "Animal welfare organizations",
  "Housing and homelessness organizations",
  "Civil rights and social justice organizations",
  "Disabilities and special needs organizations",
  "Sports and recreation organizations",
];

export const relationshipTeams = [
  {
    id: "460b02df-64aa-4fc5-b773-f936b83266bd",
    name: "CorrelAid Germany",
  },
  {
    id: "da942b5f-de2a-4d20-8a32-9921ab9923cf",
    name: "Local Chapter Konstanz",
  },
  {
    id: "9cac22bc-229b-4036-805f-f4fb7234b40f",
    name: "Local Chapter Bremen",
  },
];
export const relationshipContacts = [
  {
    id: "0618cfa8-d1ca-4af7-a189-da3bf1ba169e",
    name: "Frie",
  },
  {
    id: "9ae39299-0c10-43cd-aead-6ec69a332a52",
    name: "Isabelle",
  },
  {
    id: "18c8fae0-4062-4e86-bcc0-858d4c16b41f",
    name: "Phillip",
  },
];

type Contact = "Organization Contact" | "Project Contact";

const orgContact: Contact = "Organization Contact";
const projContact: Contact = "Project Contact";

export const sampleOrganization = {
  id: "2345a5a1-5e4a-445e-b3e8-9179c978476a",
  name: "Deutscher Caritasverband e.V.",
  legal_form: "e.V. - Eingetragener Verein",
  sector: "Community development and advocacy groups",
  relationship_team: {
    id: "460b02df-64aa-4fc5-b773-f936b83266bd",
    name: "CorrelAid Germany",
  },
  relationship_contact: {
    id: "0618cfa8-d1ca-4af7-a189-da3bf1ba169e",
    name: "Frie",
  },
  contacts: [
    {
      name: "Susie Harper",
      email: "ruw@tujep.tg",
      phone: "+49 176 2032 0211",
      type: orgContact,
    },
    {
      name: "Johnny Briggs",
      email: "ekofut@papgula.pa",
      phone: "+49 176 2032 1111",
      type: projContact,
    },
  ],
  notes:
    "Die Caritas ist mehr als eine Organisation. Sie ist eine Grundhaltung gegenüber Menschen, besonders gegenüber Menschen in Not. Wie er sieht die Caritas ihre Aufgabe darin, den Menschen ohne Ansehen von Herkunft, Status oder Religion mit Liebe und Achtung zu begegnen.",
};

export const sampleOrganizationsArray = [
  {
    id: "2345a5a1-5e4a-445e-b3e8-9179c978476a",
    name: "Deutscher Caritasverband e.V.",
  },
  {
    id: "a9e1db78-5958-41c3-b323-2870f2b75db1",
    name: "Social Entrepreneurship Netzwerk Deutschland e.V.",
  },
  {
    id: "3f6a4c64-a63b-46ac-86c8-f11ce3e9c2eb",
    name: "Deutscher Pfadfinderbund e.V.",
  },
];
