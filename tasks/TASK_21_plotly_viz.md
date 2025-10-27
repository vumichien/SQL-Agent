# TASK 21: Plotly Visualization

**Status**: Completed
**Estimated Time**: 4-6 hours
**Dependencies**: TASK 20
**Completed**: 2025-10-27

## COMPONENT

### PlotlyChart.vue
- Plotly.js integration
- Responsive container
- Dark mode sync
- Loading state

## INSTALLATION
```bash
npm install plotly.js-dist-min
```

## SUCCESS CRITERIA
- ✅ Charts render correctly (Plotly.newPlot)
- ✅ Responsive (ResizeObserver + Plotly.Plots.resize)
- ✅ Dark mode sync (MutationObserver + theme colors)
- ✅ Export working (PNG export at 1200x800, 2x scale)
- ✅ Loading state (skeleton animation)
- ✅ Error handling (with retry button)
- ✅ Refresh and reset zoom controls
- ✅ Mobile responsive design

## COMPONENT CREATED

### PlotlyChart.vue
Located: `frontend/src/components/chat/PlotlyChart.vue`

Features:
- **Plotly.js Integration**: Full Plotly.js support with newPlot API
- **Responsive Container**: ResizeObserver automatically resizes charts on container size changes
- **Theme Synchronization**: MutationObserver watches for dark mode changes and re-renders chart with theme-specific colors
- **Loading State**: Skeleton animation while chart is rendering
- **Error Handling**: Graceful error display with retry functionality
- **Export Functionality**: Export charts as PNG (1200x800px, 2x scale)
- **Chart Controls**: Refresh, reset zoom, and export buttons
- **Dark/Light Mode Support**: Automatic theme colors for backgrounds, grids, and text
- **Mobile Responsive**: Optimized button display for mobile devices

Chart Configuration:
- Responsive mode enabled
- Mode bar with common tools (zoom, pan, download)
- Removed unnecessary tools (lasso2d, select2d)
- Custom image export settings
- Auto-sizing with custom margins

Theme Colors:
- Dark mode: #1a1a1a background, #374151 grid, #e5e7eb text
- Light mode: #ffffff background, #e5e7eb grid, #1f2937 text

### Type Declarations
Located: `frontend/src/plotly.d.ts`

Type shim for plotly.js-dist-min to work with @types/plotly.js

### Integration
Integrated into `AssistantMessage.vue`:
- Replaces placeholder visualization section
- Receives figure prop from QueryResponse
- Displays when message.visualization is present

## TECHNICAL NOTES

1. **Bundle Size**: Plotly adds ~5MB to bundle (1.5MB gzipped) - this is expected for data visualization libraries
2. **Type Declarations**: Created shim to bridge plotly.js-dist-min with @types/plotly.js
3. **ResizeObserver**: Monitors container size changes for truly responsive charts
4. **MutationObserver**: Watches document.documentElement class changes to detect theme switches
5. **Lifecycle Management**: Proper cleanup with Plotly.purge in onBeforeUnmount
6. **Theme Colors**: Dynamic color scheme based on CSS variables and dark mode state
7. **Performance**: Chart only re-renders when figure prop changes or theme toggles

Dependencies:
- plotly.js-dist-min (runtime)
- @types/plotly.js (dev, for TypeScript support)

**Created**: 2025-10-27
**Completed**: 2025-10-27
