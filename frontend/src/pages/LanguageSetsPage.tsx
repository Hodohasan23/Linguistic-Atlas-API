import { useState } from "react";
import { Plus, Eye, Pencil, Trash2, GitCompareArrows, X, Tag } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from "@/components/ui/dialog";
import { mockLanguageSets, mockLanguages, type LanguageSet } from "@/data/mock";

export default function LanguageSetsPage() {
  const [sets, setSets] = useState<LanguageSet[]>(mockLanguageSets);
  const [showCreate, setShowCreate] = useState(false);
  const [compareIds, setCompareIds] = useState<[string, string] | null>(null);

  // Create form state
  const [title, setTitle] = useState("");
  const [desc, setDesc] = useState("");
  const [tagInput, setTagInput] = useState("");
  const [tags, setTags] = useState<string[]>([]);

  const handleCreate = () => {
    if (!title.trim()) return;
    const newSet: LanguageSet = {
      id: `set-${Date.now()}`,
      title,
      description: desc,
      tags,
      languageIds: [],
      createdAt: new Date().toISOString().split("T")[0],
    };
    setSets([newSet, ...sets]);
    setTitle("");
    setDesc("");
    setTags([]);
    setShowCreate(false);
  };

  const addTag = () => {
    const t = tagInput.trim().toLowerCase();
    if (t && !tags.includes(t)) {
      setTags([...tags, t]);
    }
    setTagInput("");
  };

  const handleDelete = (id: string) => {
    setSets(sets.filter((s) => s.id !== id));
  };

  // Comparison
  const compareSets = compareIds
    ? ([
        sets.find((s) => s.id === compareIds[0]),
        sets.find((s) => s.id === compareIds[1]),
      ] as [LanguageSet | undefined, LanguageSet | undefined])
    : null;

  return (
    <div className="mx-auto max-w-7xl space-y-8 px-4 py-8 sm:px-6">
      <div className="flex items-start justify-between">
        <div>
          <h1 className="font-display text-3xl font-bold tracking-tight text-foreground">
            Language Sets
          </h1>
          <p className="mt-1 text-muted-foreground">
            Organise and compare groups of languages
          </p>
        </div>
        <Button onClick={() => setShowCreate(true)}>
          <Plus className="mr-1.5 h-4 w-4" /> Create Set
        </Button>
      </div>

      {/* Create dialog */}
      <Dialog open={showCreate} onOpenChange={setShowCreate}>
        <DialogContent className="max-w-md">
          <DialogHeader>
            <DialogTitle className="font-display text-xl">New Language Set</DialogTitle>
            <DialogDescription>Create a custom set for comparison and analysis.</DialogDescription>
          </DialogHeader>
          <div className="space-y-4 pt-2">
            <Input placeholder="Title" value={title} onChange={(e) => setTitle(e.target.value)} />
            <Textarea
              placeholder="Description"
              value={desc}
              onChange={(e) => setDesc(e.target.value)}
              rows={3}
            />
            <div>
              <div className="flex gap-2">
                <Input
                  placeholder="Add tag…"
                  value={tagInput}
                  onChange={(e) => setTagInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && (e.preventDefault(), addTag())}
                />
                <Button variant="outline" size="sm" onClick={addTag} type="button">
                  <Tag className="h-4 w-4" />
                </Button>
              </div>
              {tags.length > 0 && (
                <div className="mt-2 flex flex-wrap gap-1.5">
                  {tags.map((t) => (
                    <Badge key={t} variant="secondary" className="gap-1">
                      {t}
                      <X
                        className="h-3 w-3 cursor-pointer"
                        onClick={() => setTags(tags.filter((x) => x !== t))}
                      />
                    </Badge>
                  ))}
                </div>
              )}
            </div>
            <Button className="w-full" onClick={handleCreate}>
              Create Set
            </Button>
          </div>
        </DialogContent>
      </Dialog>

      {/* Sets grid */}
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {sets.map((set) => (
          <Card key={set.id} className="rounded-2xl shadow-sm transition-shadow hover:shadow-lg">
            <CardHeader className="pb-3">
              <CardTitle className="font-display text-lg">{set.title}</CardTitle>
              <p className="text-sm text-muted-foreground line-clamp-2">{set.description}</p>
            </CardHeader>
            <CardContent className="space-y-4">
              <div className="flex flex-wrap gap-1.5">
                {set.tags.map((t) => (
                  <Badge key={t} variant="secondary" className="text-xs">
                    {t}
                  </Badge>
                ))}
              </div>
              <p className="text-sm text-muted-foreground">
                {set.languageIds.length} language{set.languageIds.length !== 1 ? "s" : ""}
              </p>
              <div className="flex flex-wrap gap-2">
                <Button variant="outline" size="sm">
                  <Eye className="mr-1 h-3.5 w-3.5" /> View
                </Button>
                <Button variant="outline" size="sm">
                  <Pencil className="mr-1 h-3.5 w-3.5" /> Edit
                </Button>
                <Button
                  variant="outline"
                  size="sm"
                  className="text-destructive hover:text-destructive"
                  onClick={() => handleDelete(set.id)}
                >
                  <Trash2 className="mr-1 h-3.5 w-3.5" /> Delete
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Compare section */}
      {sets.length >= 2 && (
        <Card className="rounded-2xl shadow-sm">
          <CardHeader>
            <CardTitle className="font-display text-lg flex items-center gap-2">
              <GitCompareArrows className="h-5 w-5 text-primary" />
              Compare Sets
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div className="flex flex-col gap-3 sm:flex-row">
              <select
                className="flex-1 rounded-lg border bg-background px-3 py-2 text-sm"
                onChange={(e) =>
                  setCompareIds((prev) => [e.target.value, prev?.[1] || sets[1]?.id || ""])
                }
                defaultValue=""
              >
                <option value="" disabled>
                  Select Set A
                </option>
                {sets.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.title}
                  </option>
                ))}
              </select>
              <select
                className="flex-1 rounded-lg border bg-background px-3 py-2 text-sm"
                onChange={(e) =>
                  setCompareIds((prev) => [prev?.[0] || sets[0]?.id || "", e.target.value])
                }
                defaultValue=""
              >
                <option value="" disabled>
                  Select Set B
                </option>
                {sets.map((s) => (
                  <option key={s.id} value={s.id}>
                    {s.title}
                  </option>
                ))}
              </select>
            </div>

            {compareSets && compareSets[0] && compareSets[1] && (
              <ComparePanel a={compareSets[0]} b={compareSets[1]} />
            )}
          </CardContent>
        </Card>
      )}
    </div>
  );
}

function ComparePanel({ a, b }: { a: LanguageSet; b: LanguageSet }) {
  const langsA = mockLanguages.filter((l) => a.languageIds.includes(l.id));
  const langsB = mockLanguages.filter((l) => b.languageIds.includes(l.id));
  const shared = langsA.filter((l) => b.languageIds.includes(l.id));
  const uniqueA = langsA.filter((l) => !b.languageIds.includes(l.id));
  const uniqueB = langsB.filter((l) => !a.languageIds.includes(l.id));

  const familiesA = new Set(langsA.map((l) => l.family));
  const familiesB = new Set(langsB.map((l) => l.family));

  return (
    <div className="rounded-xl border bg-muted/30 p-5 space-y-4">
      <h3 className="font-display text-base font-semibold text-foreground">Comparison Insights</h3>
      <div className="grid gap-4 sm:grid-cols-2">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            {a.title}
          </p>
          <p className="text-sm">{langsA.length} languages · {familiesA.size} families</p>
          <p className="text-xs text-muted-foreground mt-1">
            Unique: {uniqueA.map((l) => l.name).join(", ") || "None"}
          </p>
        </div>
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
            {b.title}
          </p>
          <p className="text-sm">{langsB.length} languages · {familiesB.size} families</p>
          <p className="text-xs text-muted-foreground mt-1">
            Unique: {uniqueB.map((l) => l.name).join(", ") || "None"}
          </p>
        </div>
      </div>
      <div className="rounded-lg border bg-card p-3">
        <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Shared Languages
        </p>
        <p className="text-sm mt-1">
          {shared.length > 0 ? shared.map((l) => l.name).join(", ") : "No overlap between these sets"}
        </p>
      </div>
      <div className="rounded-lg border bg-card p-3">
        <p className="text-xs font-medium uppercase tracking-wider text-muted-foreground">
          Insight
        </p>
        <p className="text-sm mt-1 text-muted-foreground">
          {shared.length > 0
            ? `These sets share ${shared.length} language${shared.length > 1 ? "s" : ""}, suggesting overlapping research focus in ${[...new Set(shared.map((l) => l.macroarea))].join(" and ")}.`
            : `No overlap detected — these sets cover entirely distinct language groups, ideal for broadening comparative scope.`}
        </p>
      </div>
    </div>
  );
}
