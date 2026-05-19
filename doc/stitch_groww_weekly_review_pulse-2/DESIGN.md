---
name: Pulse Analytics
colors:
  surface: '#fbf8ff'
  surface-dim: '#d7d8f1'
  surface-bright: '#fbf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f2ff'
  surface-container: '#ececff'
  surface-container-high: '#e5e6ff'
  surface-container-highest: '#dfe1fa'
  on-surface: '#171a2c'
  on-surface-variant: '#3c4a43'
  inverse-surface: '#2c2f42'
  inverse-on-surface: '#f0efff'
  outline: '#6b7b72'
  outline-variant: '#bacac1'
  surface-tint: '#006c4f'
  primary: '#006c4f'
  on-primary: '#ffffff'
  primary-container: '#00d09c'
  on-primary-container: '#00533c'
  inverse-primary: '#2fe0aa'
  secondary: '#5f5e60'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfe1'
  on-secondary-container: '#636264'
  tertiary: '#934b07'
  on-tertiary: '#ffffff'
  tertiary-container: '#ffa15b'
  on-tertiary-container: '#733800'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#59fdc5'
  primary-fixed-dim: '#2fe0aa'
  on-primary-fixed: '#002116'
  on-primary-fixed-variant: '#00513b'
  secondary-fixed: '#e4e2e4'
  secondary-fixed-dim: '#c8c6c8'
  on-secondary-fixed: '#1b1b1d'
  on-secondary-fixed-variant: '#474649'
  tertiary-fixed: '#ffdcc6'
  tertiary-fixed-dim: '#ffb785'
  on-tertiary-fixed: '#301400'
  on-tertiary-fixed-variant: '#713700'
  background: '#fbf8ff'
  on-background: '#171a2c'
  surface-variant: '#dfe1fa'
  primary-hover: '#00B88A'
  page-bg: '#F6F7F9'
  card-surface: '#FFFFFF'
  border-subtle: '#E9E9EB'
  text-muted: '#7C7E8C'
  status-success: '#00D09C'
  status-warning: '#F5A623'
  status-error: '#DF514C'
  status-info: '#5367FF'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 21px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  sidebar-width: 240px
  max-content-width: 1200px
  gutter: 24px
  card-padding: 24px
---

## Brand & Style
The design system is engineered for executive-level clarity and financial precision. It follows a **Modern Corporate** aesthetic characterized by high-density information presented through a lens of extreme minimalism. The goal is to facilitate "speed to insight," allowing leadership to scan complex datasets in under two minutes without visual fatigue.

The visual narrative avoids the aggressive urgency typical of trading platforms, opting instead for a calm, trustworthy environment. It utilizes generous whitespace, a strictly controlled color palette, and soft geometric shapes to create a workspace that feels reliable, objective, and sophisticated.

## Colors
The palette is anchored by a high-vibrancy "Investment Green" used exclusively for positive reinforcement and primary actions. 

- **Primary & Success:** The green (#00D09C) is the workhorse of the system, representing growth and "go" states.
- **Surface Strategy:** We use a layered neutral approach. The page background is a cool off-white (#F6F7F9) to provide enough contrast for white card surfaces to "pop" without relying on heavy shadows.
- **Typography Hierarchy:** Deep charcoal (#1D1D1F) is reserved for headers to ensure maximum legibility, while a softer slate (#44475B) handles body text to reduce glare during extended reading.

## Typography
The system utilizes **Inter** for its exceptional legibility in data-dense environments and its neutral, modern character. 

- **Headlines:** Use semibold weights with slight negative letter-spacing for a tight, professional appearance in titles.
- **Data Points:** Large metrics in cards should use `headline-xl` to ensure they are the first thing a user sees.
- **Captions:** Used for metadata, timestamps, and secondary axis labels in charts. These are always rendered in the muted text color to maintain hierarchy.

## Layout & Spacing
This design system employs a **Fixed-Fluid Hybrid Grid**. The content is contained within a 1200px centered wrapper to prevent line lengths from becoming unreadable on ultra-wide monitors.

- **Sidebar:** A persistent 240px left-hand navigation provides structural grounding.
- **Grid:** A strict 8px linear scale governs all margins and padding. 
- **Desktop:** 12-column grid with 24px gutters.
- **Tablet:** 6-column grid with 16px gutters.
- **Mobile:** Single column with 16px side margins; metrics stack vertically.

## Elevation & Depth
Depth is communicated through **Subtle Ambient Shadows** rather than heavy borders or high-contrast offsets. 

- **Level 0 (Background):** The `#F6F7F9` canvas.
- **Level 1 (Cards):** White surfaces with a very soft `0 1px 3px rgba(0,0,0,0.06)` shadow. This creates a "lifted" appearance that distinguishes interactive data modules from the background.
- **Level 2 (Dropdowns/Modals):** A more pronounced shadow `0 4px 12px rgba(0,0,0,0.1)` to indicate temporary overlays.
- **Dividers:** Use 1px solid `#E9E9EB` for internal card divisions only.

## Shapes
The shape language is "Soft Geometric." It uses medium-radius corners to strike a balance between the precision of fintech (sharp) and the approachability of a internal review tool (rounded).

- **Data Cards:** 12px corner radius for a modern, containerized look.
- **Interactive Elements:** Buttons and Input fields use an 8px radius to feel distinct from the structural cards.
- **Indicators:** Progress bars and chips use fully rounded (pill) ends to differentiate them from functional containers.

## Components

### Buttons
- **Primary:** Solid `#00D09C` fill with `#FFFFFF` text. No border. On hover, darken to `#00B88A`.
- **Secondary:** White fill with a 1px `#00D09C` border and `#00D09C` text. Used for less critical actions.

### Status Chips
Small, pill-shaped indicators with subtle background tints:
- **Passed:** Green text on 10% opacity green background.
- **Pending:** Gray text on 10% opacity gray background.
- **Failed:** Red text on 10% opacity red background.

### Data Cards
The core dashboard element. Must include:
- A clear title in `body-md` (Muted Text).
- A primary metric in `headline-xl` (Primary Dark).
- A trend indicator (small green/red arrow + percentage) positioned next to the metric.

### Data Visualization
- **Horizontal Bar Charts:** Use `#00D09C` for the active bar value and `#E9E9EB` for the background track. Bar ends must be rounded (pill-shaped).
- **Tooltips:** Dark gray background with white text, 4px border radius.

### External Link Cards
Standard card styling but includes a 32px monochromatic icon (e.g., Google Sheets or Gmail logo) on the left, a title, and a small "arrow-up-right" icon to signal an external jump.