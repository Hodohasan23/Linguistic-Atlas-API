import { apiFetch } from "@/api/config";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { ChevronLeft, ChevronRight, Filter, Search } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

type Language = {
  id: string;
  name: string;
  macroarea: string | null;
  countries: string | null;
  family_id: string | null;
  iso_code: string | null;
  glottocode: string | null;
  level: string | null;
  latitude: number | null;
  longitude: number | null;
  is_isolate: boolean | string | null;
  first_year_of_documentation: number | null;
  last_year_of_documentation: number | null;
};

const PAGE_SIZE = 8;

const MACROAREAS = [
  "Africa",
  "Eurasia",
  "Papunesia",
  "North America",
  "South America",
  "Australia",
];

const LEVELS = ["family", "language", "dialect"];

const MACROAREA_COLORS: Record<string, string> = {
  Africa: "#C96B4B",
  Eurasia: "#7A8F6A",
  Papunesia: "#8E6BBE",
  "North America": "#4C9BE8",
  "South America": "#2A9D8F",
  Australia: "#E9A03B",
};

export default function LanguagesPage() {
  const [languages, setLanguages] = useState<Language[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [search, setSearch] = useState("");
  const [macroarea, setMacroarea] = useState("all");
  const [level, setLevel] = useState("all");
  const [selected, setSelected] = useState<Language | null>(null);
  const [page, setPage] = useState(1);

  useEffect(() => {
    async function loadLanguages() {
      try {
        setLoading(true);
        setError(null);
        const data = await apiFetch<Language[]>("/languages?limit=100&offset=0");
        setLanguages(data);
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to load languages");
      } finally {
        setLoading(false);
      }
    }

    loadLanguages();
  }, []);

  const filtered = useMemo(() => {
    return languages.filter((l) => {
      const name = l.name ?? "";
      const isoCode = l.iso_code ?? "";
      const macro = l.macroarea ?? "";
      const currentLevel = l.level ?? "";

      const matchSearch =
        name.toLowerCase().includes(search.toLowerCase()) ||
        isoCode.toLowerCase().includes(search.toLowerCase());

      const matchMacro = macroarea === "all" || macro.includes(macroarea);
      const matchLevel =
        level === "all" || currentLevel.toLowerCase() === level.toLowerCase();

      return matchSearch && matchMacro && matchLevel;
    });
  }, [languages, search, macroarea, level]);

  useEffect(() => {
    setPage(1);
  }, [search, macroarea, level]);

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE);
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  return (
    <div className="mx-auto max-w-7xl space-y-6 px-4 py-8 sm:px-6">
      <div>
        <h1 className="font-display text-3xl font-bold tracking-tight text-foreground">
          Languages
        </h1>
        <p className="mt-1 text-muted-foreground">
          Browse and search the linguistic database
        </p>
      </div>

      <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
        <div className="relative flex-1">
          <Search className="absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-muted-foreground" />
          <Input
            placeholder="Search by name or ISO code…"
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-10"
          />
        </div>

        <Select value={macroarea} onValueChange={setMacroarea}>
          <SelectTrigger className="w-full sm:w-[180px]">
            <Filter className="mr-2 h-4 w-4 text-muted-foreground" />
            <SelectValue placeholder="Macroarea" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Macroareas</SelectItem>
            {MACROAREAS.map((m) => (
              <SelectItem key={m} value={m}>
                {m}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>

        <Select value={level} onValueChange={setLevel}>
          <SelectTrigger className="w-full sm:w-[160px]">
            <SelectValue placeholder="Level" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="all">All Levels</SelectItem>
            {LEVELS.map((l) => (
              <SelectItem key={l} value={l} className="capitalize">
                {l}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {loading && <p className="text-sm text-muted-foreground">Loading languages...</p>}
      {error && <p className="text-sm text-destructive">{error}</p>}

      {!loading && !error && (
        <>
          <p className="text-sm text-muted-foreground">
            {filtered.length} language{filtered.length !== 1 ? "s" : ""} found
          </p>

          <div className="rounded-2xl border bg-card shadow-sm">
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Name</TableHead>
                  <TableHead>Macroarea</TableHead>
                  <TableHead className="hidden md:table-cell">Country</TableHead>
                  <TableHead className="hidden lg:table-cell">Family</TableHead>
                  <TableHead className="text-right">Action</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {paginated.map((lang) => (
                  <TableRow key={lang.id} className="transition-colors hover:bg-muted/50">
                    <TableCell className="font-medium">{lang.name}</TableCell>
                    <TableCell>
                      <Badge
                        variant="secondary"
                        style={{
                          borderLeft: `3px solid ${
                            MACROAREA_COLORS[lang.macroarea ?? ""] ?? "#999"
                          }`,
                        }}
                        className="rounded-md"
                      >
                        {lang.macroarea ?? "Unknown"}
                      </Badge>
                    </TableCell>
                    <TableCell className="hidden md:table-cell">
                      {lang.countries ?? "—"}
                    </TableCell>
                    <TableCell className="hidden lg:table-cell text-muted-foreground">
                      {lang.family_id ?? "—"}
                    </TableCell>
                    <TableCell className="text-right">
                      <Button variant="outline" size="sm" onClick={() => setSelected(lang)}>
                        View
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}

                {paginated.length === 0 && (
                  <TableRow>
                    <TableCell colSpan={5} className="py-12 text-center text-muted-foreground">
                      No languages match your filters.
                    </TableCell>
                  </TableRow>
                )}
              </TableBody>
            </Table>
          </div>

          {totalPages > 1 && (
            <div className="flex items-center justify-center gap-2">
              <Button
                variant="outline"
                size="sm"
                disabled={page <= 1}
                onClick={() => setPage((p) => p - 1)}
              >
                <ChevronLeft className="h-4 w-4" /> Prev
              </Button>
              <span className="text-sm text-muted-foreground">
                Page {page} of {totalPages}
              </span>
              <Button
                variant="outline"
                size="sm"
                disabled={page >= totalPages}
                onClick={() => setPage((p) => p + 1)}
              >
                Next <ChevronRight className="h-4 w-4" />
              </Button>
            </div>
          )}
        </>
      )}

      <Dialog open={!!selected} onOpenChange={() => setSelected(null)}>
        <DialogContent className="max-w-lg">
          {selected && (
            <>
              <DialogHeader>
                <DialogTitle className="font-display text-2xl">
                  {selected.name}
                </DialogTitle>
                <DialogDescription>
                  Explore language metadata and geographic information
                </DialogDescription>
              </DialogHeader>

              <div className="grid grid-cols-2 gap-4 pt-4">
                <InfoItem label="ISO 639-3" value={selected.iso_code ?? "—"} mono />
                <InfoItem label="Glottocode" value={selected.glottocode ?? "—"} mono />
                <InfoItem label="Family ID" value={selected.family_id ?? "—"} />
                <InfoItem label="Macroarea" value={selected.macroarea ?? "—"} />
                <InfoItem label="Country" value={selected.countries ?? "—"} />
                <InfoItem label="Level" value={selected.level ?? "—"} />
                <InfoItem
                  label="Isolate"
                  value={String(selected.is_isolate ?? "—")}
                />
                <InfoItem
                  label="Documentation"
                  value={
                    selected.first_year_of_documentation && selected.last_year_of_documentation
                      ? `${selected.first_year_of_documentation}–${selected.last_year_of_documentation}`
                      : "—"
                  }
                />

                <div className="col-span-2">
                  <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                    Coordinates
                  </p>
                  <p className="mt-0.5 font-mono text-sm">
                    {selected.latitude != null && selected.longitude != null
                      ? `${selected.latitude.toFixed(4)}, ${selected.longitude.toFixed(4)}`
                      : "—"}
                  </p>
                </div>
              </div>
            </>
          )}
        </DialogContent>
      </Dialog>
    </div>
  );
}

function InfoItem({
  label,
  value,
  mono,
}: {
  label: string;
  value: string;
  mono?: boolean;
}) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
        {label}
      </p>
      <p className={`mt-0.5 text-sm ${mono ? "font-mono" : ""}`}>{value}</p>
    </div>
  );
}
