export function load({ url }) {
  const brukernavn =
    url.searchParams.get("brukernavn") || "fant ikke brukernavn";
  const tillatelse =
    url.searchParams.get("tillatelse") || "fant ikke tillatelse";
  const id = url.searchParams.get("id") || "fant ikke id";
  return { brukernavn, tillatelse, id };
}
