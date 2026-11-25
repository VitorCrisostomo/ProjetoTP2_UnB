import { renderToStaticMarkup } from "react-dom/server";
import { expect, it } from "vitest";
import RootLayout from "@/app/layout";

it("define o idioma da página e preserva seu conteúdo", () => {
  const html = renderToStaticMarkup(
    <RootLayout>
      <p>Conteúdo de teste</p>
    </RootLayout>,
  );
  const document = new DOMParser().parseFromString(html, "text/html");
  expect(document.documentElement.lang).toBe("pt-BR");
  expect(document.body.textContent).toBe("Conteúdo de teste");
});
