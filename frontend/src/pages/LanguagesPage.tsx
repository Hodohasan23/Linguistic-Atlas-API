import { useState, useMemo } from "react";
import { Search, Filter, ChevronLeft, ChevronRight } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "@/components/ui/select";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { Badge } from "@/components/ui/badge";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { mockLanguages, MACROAREAS, LEVELS, MACROAREA_COLORS, type Language } from "@/data/mock";

const PAGE_SIZE = 8;

export default function LanguagesPage() {
  const [search, setSearch] = useState("");
  const [macroarea, setMacroarea] = useState("all");
  const [level, setLevel] = useState("all");
  const [selected, setSelected] = useState<Language | null>(null);
  const [page, setPage] = useState(1);

  const filtered = useMemo(() => {
    return mockLanguages.filter((l) => {
      const matchSearch =
        l.name.toLowerCase().includes(search.toLowerCase()) ||
        l.isoCode.toLowerCase().includes(search.toLowerCase());
      const matchMacro = macroarea === "all" || l.macroarea === macroarea;
      const matchLevel = level === "all" || l.level === level;
      return matchSearch && matchMacro && matchLevel;
    });
  }, [search, macroarea, level]);

  const totalPages = Math.ceil(filtered.length / PAGE_SIZE);
  const paginated = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  // Reset page when filters change
  useMemo(() => setPage(1), [search, macroarea, level]);

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

      {/* Filters */}
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
              <SelectItem key={m} value={m}>{m}</SelectItem>
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
              <SelectItem key={l} value={l} className="capitalize">{l}</SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>

      {/* Results count */}
      <p className="text-sm text-muted-foreground">
        {filtered.length} language{filtered.length !== 1 ? "s" : ""} found
      </p>

      {/* Table */}
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
                    style={{ borderLeft: `3px solid ${MACROAREA_COLORS[lang.macroarea]}` }}
                    className="rounded-md"
                  >
                    {lang.macroarea}
                  </Badge>
                </TableCell>
                <TableCell className="hidden md:table-cell">{lang.country}</TableCell>
                <TableCell className="hidden lg:table-cell text-muted-foreground">
                  {lang.family}
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

      {/* Pagination */}
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

      {/* Detail Modal */}
      <Dialog open={!!selected} onOpenChange={() => setSelected(null)}>
        <DialogContent className="max-w-lg">
          {selected && (
            <>
              <DialogHeader>
                <DialogTitle className="font-display text-2xl">{selected.name}</DialogTitle>
                <DialogDescription>{selected.description}</DialogDescription>
              </DialogHeader>
              <div className="grid grid-cols-2 gap-4 pt-4">
                <InfoItem label="ISO 639-3" value={selected.isoCode} mono />
                <InfoItem label="Glottocode" value={selected.glottocode} mono />
                <InfoItem label="Family" value={selected.family} />
                <InfoItem label="Macroarea" value={selected.macroarea} />
                <InfoItem label="Country" value={selected.country} />
                <InfoItem label="Level" value={selected.level} />
                <InfoItem label="Speakers" value={selected.speakers.toLocaleString()} />
                <InfoItem label="Status" value={selected.status} />
                <div className="col-span-2">
                  <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
                    Coordinates
                  </p>
                  <p className="mt-0.5 font-mono text-sm">
                    {selected.latitude.toFixed(4)}, {selected.longitude.toFixed(4)}
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

function InfoItem({ label, value, mono }: { label: string; value: string; mono?: boolean }) {
  return (
    <div>
      <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">{label}</p>
      <p className={`mt-0.5 text-sm ${mono ? "font-mono" : ""}`}>{value}</p>
    </div>
  );
}
