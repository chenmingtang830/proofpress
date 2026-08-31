const revealItems = document.querySelectorAll(".reveal");

if ("IntersectionObserver" in window && !window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return;
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      });
    },
    { threshold: 0.12 },
  );

  revealItems.forEach((item) => observer.observe(item));
} else {
  revealItems.forEach((item) => item.classList.add("is-visible"));
}

const partnerForm = document.querySelector("#partner-form");

partnerForm?.addEventListener("submit", (event) => {
  event.preventDefault();

  if (!partnerForm.reportValidity()) return;

  const data = new FormData(partnerForm);
  const repository = partnerForm.dataset.githubRepo;
  const team = data.get("team").trim();
  const workflow = data.get("workflow").trim();
  const decision = data.get("decision").trim();
  const next = data.get("next");
  const title = `Design partner workflow: ${team}`;
  const body = [
    "## Workflow",
    workflow,
    "",
    "## Downstream decision",
    decision,
    "",
    "## What would be useful next?",
    next,
    "",
    "## Disclosure check",
    "- [x] I have not included confidential, privileged, personal, or customer data",
  ].join("\n");

  const issueUrl = new URL(`https://github.com/${repository}/issues/new`);
  issueUrl.searchParams.set("labels", "design-partner");
  issueUrl.searchParams.set("title", title);
  issueUrl.searchParams.set("body", body);
  window.open(issueUrl.toString(), "_blank", "noopener,noreferrer");
});
