# Homelab Dark Theme Style Guide

This is the official style guide for all homelab web applications. It ensures a consistent dark theme experience across your home network.

## Color Palette

### Primary Colors (Dark Green Theme)
```css
--primary-color: #003314;      /* Main accent - dark green */
--primary-light: #005522;      /* Hover states */
--primary-dark: #001a0a;       /* Darker variant */
```

### Background Colors
```css
--bg-primary: #1a1a1a;         /* Page background */
--bg-secondary: #2a2a2a;       /* Cards, sections, navbar */
--bg-tertiary: #3a3a3a;        /* Input fields, buttons */
--bg-hover: #444444;           /* Hover states */
```

### Text Colors
```css
--text-primary: #ffffff;       /* Main headings, body text */
--text-secondary: #cccccc;     /* Descriptions, meta info */
--text-muted: #999999;         /* Timestamps, subtle info */
```

### Utility Colors
```css
--border-color: #444444;
--success: #28a745;
--warning: #ffc107;
--danger: #dc3545;
```

## Typography

### Font Family
```css
font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
```

### Font Sizes
- **Small**: 0.875rem (14px) - Timestamps, meta info
- **Base**: 1rem (16px) - Body text
- **Large**: 1.125rem (18px) - Descriptions
- **XL**: 1.5rem (24px) - Section headings
- **XXL**: 2rem (32px) - Page titles

## Spacing Scale

Use consistent spacing:
- **XS**: 0.25rem (4px)
- **SM**: 0.5rem (8px)
- **MD**: 1rem (16px)
- **LG**: 1.5rem (24px)
- **XL**: 2rem (32px)
- **XXL**: 3rem (48px)

## Border Radius

- **Small**: 4px - Buttons, inputs
- **Medium**: 8px - Cards, sections
- **Large**: 12px - Larger containers
- **Full**: 9999px - Pills, tags

## Component Examples

### Navigation Bar
- Background: `--bg-secondary`
- Border bottom: 2px solid `--primary-color`
- Logo color: `--primary-color` with glow effect
- Link color: `--text-primary`, hover: `--primary-color`

### Buttons

#### Primary Button
```css
background: var(--primary-color);
color: var(--text-primary);
hover: transform: translateY(-1px) + shadow
```

#### Secondary Button
```css
background: var(--bg-tertiary);
color: var(--text-primary);
```

#### Danger Button
```css
background: var(--danger);
color: var(--text-primary);
```

### Cards
- Background: `--bg-secondary`
- Border: 1px solid `--border-color`
- Border radius: 8px
- Shadow: subtle dark shadow
- Hover: lift up 4px, green shadow, border changes to `--primary-color`

### Forms
- Input background: `--bg-tertiary`
- Border: 1px solid `--border-color`
- Focus: border changes to `--primary-color` with green shadow
- Text color: `--text-primary`

### Tags/Pills
- Background: `--primary-dark`
- Border: 1px solid `--primary-color`
- Text color: `--primary-color`
- Border radius: full (pill shape)

## Design Principles

1. **Readability First**: White text on dark backgrounds for optimal reading
2. **Consistent Accents**: Use #003314 (dark green) for all interactive elements
3. **Subtle Shadows**: Use rgba(0, 51, 20, 0.3) for green-tinted shadows
4. **Smooth Transitions**: 0.2s for hovers, 0.3s for major state changes
5. **Hierarchy**: Use text colors (primary > secondary > muted) to establish visual hierarchy

## Accessibility

- **Contrast Ratios**:
  - White text (#ffffff) on dark backgrounds meets WCAG AA standards
  - Primary green (#003314) provides sufficient contrast for accents
- **Focus States**: Always include visible focus indicators with green glow
- **Touch Targets**: Minimum 44x44px for mobile interactions

## Usage in New Projects

### Quick Start
1. Copy the CSS variables from `style.css` (lines 4-48)
2. Apply base styles (body, container)
3. Use the component classes as needed

### File Structure
```
your-app/
├── static/
│   └── css/
│       └── style.css  (copy from ShoreLunch)
└── templates/
    └── base.html      (navbar + footer)
```

### Navbar Template
```html
<nav class="navbar">
    <div class="container">
        <a href="/" class="logo">Your App Name</a>
        <ul class="nav-menu">
            <li><a href="/">Home</a></li>
            <!-- Add your menu items -->
        </ul>
    </div>
</nav>
```

### Footer Template
```html
<footer>
    <div class="container">
        <p>&copy; 2026 Your Homelab</p>
    </div>
</footer>
```

## Examples from ShoreLunch

This style guide is implemented in the ShoreLunch recipe app. Reference these files:
- **CSS**: `/app/static/css/style.css`
- **Base Template**: `/app/templates/base.html`
- **Card Example**: Recipe cards on homepage
- **Form Example**: Recipe creation form
- **Detail Page Example**: Recipe detail view

## Customization

To adapt this theme for different apps while maintaining consistency:

1. **Keep the same**:
   - Primary color (#003314)
   - Background colors
   - Text colors
   - Spacing scale

2. **Can adjust**:
   - Font sizes for specific use cases
   - Card layouts based on content
   - Component-specific styling

## Mobile Responsiveness

Always include these breakpoints:
```css
@media (max-width: 768px) {
    /* Mobile adjustments */
    .navbar .container { flex-direction: column; }
    .recipe-grid { grid-template-columns: 1fr; }
}
```

## Version

**Version 1.0** - Initial dark theme for ShoreLunch (2026-02-01)

---

*This style guide ensures all your homelab applications have a consistent, professional dark theme with excellent readability.*
