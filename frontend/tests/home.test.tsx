import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import Home from "@/app/page";

describe("página inicial", () => {
  it("apresenta o projeto e informa que as funcionalidades estão em desenvolvimento", () => {
    render(<Home />);
    expect(
      screen.getByRole("heading", { level: 1, name: "Sistema de ocorrências" }),
    ).toBeInTheDocument();
    expect(screen.getByText(/Funcionalidades em desenvolvimento/)).toBeVisible();
  });
});
