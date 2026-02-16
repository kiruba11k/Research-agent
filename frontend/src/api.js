const API = import.meta.env.VITE_API_BASE;

export async function runResearch(formData) {
  const res = await fetch(`${API}/research`, {
    method: "POST",
    body: formData
  });
  return res.json();
}
