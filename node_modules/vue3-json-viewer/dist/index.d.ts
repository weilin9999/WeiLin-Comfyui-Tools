import { App } from 'vue';
import { default as JsonViewer, JsonViewerProps } from './Components/json-viewer.vue';
/**
 * The main JsonViewer Vue component.
 * @see JsonViewerProps for a detailed list of available props.
 * @example
 * ```vue
 * <template>
 *   <JsonViewer :value="jsonData" theme="jv-dark" />
 * </template>
 * <script setup>
 *   import { JsonViewer } from "vue3-json-viewer";
 *   import "vue3-json-viewer/dist/style.css"; // Or your own theme
 *
 *   const jsonData = { a: 1, b: { c: 2 } };
 * <\/script>
 * ```
 */
export { JsonViewer };
/**
 * Type definition for the props accepted by the {@link JsonViewer} component.
 */
export type { JsonViewerProps };
/**
 * Default export for Vue plugin usage (e.g., `app.use(Vue3JsonViewer)`).
 */
declare const _default: {
    install: (app: App) => void;
};
export default _default;
