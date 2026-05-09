// Wire up Tablesort on every <article> table without an explicit class.
// Reinitializes on Material's instant-navigation events so it survives
// SPA-style page transitions (navigation.instant).
//
// Recipe straight from
// https://squidfunk.github.io/mkdocs-material/reference/data-tables/

document$.subscribe(function () {
  var tables = document.querySelectorAll("article table:not([class])");
  tables.forEach(function (table) {
    new Tablesort(table);
  });
});
