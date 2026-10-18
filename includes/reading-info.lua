-- Add static reading details to longer web notes when Quarto builds the site.
function Pandoc(doc)
  if not FORMAT:match("html") then return end

  local title_index
  for i, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 1 then
      if block.identifier == "about" or
          block.identifier == "introducing-four-case-studies" then return end
      title_index = i
      break
    end
  end
  if not title_index then return end

  local text = doc:walk({
    Div = function(block)
      if block.classes:includes("note-disclaimer") then return {} end
    end,
    Note = function(note)
      return pandoc.Str(" " .. pandoc.utils.stringify(note.content) .. " ")
    end,
    Span = function(span)
      if span.classes:includes("note-subtitle") then return {} end
    end
  })
  local words, skip_level = 0, nil
  for _, block in ipairs(text.blocks) do
    if block.t == "Header" then
      if block.identifier:match("^references") or
          block.identifier:match("^further-reading") then
        skip_level = block.level
      elseif skip_level and block.level <= skip_level then
        skip_level = nil
      end
    end
    if not skip_level and not (block.t == "Header" and block.level == 1) then
      for word in pandoc.utils.stringify(block):gmatch("%S+") do
        if word:match("%w") then words = words + 1 end
      end
    end
  end
  if words < 500 then return end

  local info = string.format("%d words · %d min read",
    math.floor(words / 100 + 0.5) * 100, math.ceil(words / 200))
  table.insert(doc.blocks, title_index, pandoc.RawBlock("html",
    '<p class="note-reading-info">' .. info .. '</p>'))
  return doc
end
