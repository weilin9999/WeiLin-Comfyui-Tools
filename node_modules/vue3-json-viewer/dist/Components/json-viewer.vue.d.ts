import { PropType } from 'vue';
import { default as JsonBox } from './json-box.vue';
interface CopyableOptions {
    copyText?: string;
    copiedText?: string;
    timeout?: number;
    align?: 'left' | 'right';
}
interface JsonBoxComponent extends InstanceType<typeof JsonBox> {
    $el: HTMLElement;
}
interface ClipElement extends HTMLElement {
}
/**
 * Props for the JsonViewer component.
 */
export interface JsonViewerProps {
    /** The JSON object or array to display. Can also be a string, number, boolean, or function. */
    value: any;
    /** Whether the JSON tree should be initially expanded. */
    expanded?: boolean;
    /** The initial depth to expand the JSON tree. */
    expandDepth?: number;
    /**
     * Enables copying the JSON data.
     * Can be a boolean or an object with `CopyableOptions`.
     */
    copyable?: boolean | CopyableOptions;
    /** Whether to sort object keys alphabetically. */
    sort?: boolean;
    /** Whether to display the viewer in a boxed mode with a border. */
    boxed?: boolean;
    /** The theme for the viewer, e.g., 'light' or 'dark'. */
    theme?: string;
    /** A function to format date values. */
    timeformat?: (value: Date) => string;
    /** Whether to enable preview mode, which might show a condensed view. */
    previewMode?: boolean;
    /** Whether to attempt parsing the `value` prop if it's a string. */
    parse?: boolean;
}
/**
 * JsonViewer is a Vue component for displaying JSON data in a collapsible tree structure.
 * It supports various data types, copying to clipboard, themes, and custom styling.
 */
declare const _default: import('vue').DefineComponent<{
    value: any;
    expanded?: boolean | undefined;
    expandDepth?: number | undefined;
    copyable?: (boolean | CopyableOptions) | undefined;
    sort?: boolean | undefined;
    boxed?: boolean | undefined;
    theme?: string | undefined;
    timeformat?: ((value: Date) => string) | undefined;
    previewMode?: boolean | undefined;
    parse?: boolean | undefined;
}, {
    clip: import('vue').Ref<ClipElement | null, ClipElement | null>;
    jsonBox: import('vue').Ref<JsonBoxComponent | null, JsonBoxComponent | null>;
    copied: import('vue').Ref<boolean, boolean>;
    expandableCode: import('vue').Ref<boolean, boolean>;
    expandCode: import('vue').Ref<boolean | undefined, boolean | undefined>;
    jvClass: import('vue').ComputedRef<string>;
    copyText: import('vue').ComputedRef<{
        copyText: string;
        copiedText: string;
        timeout: number;
        align: "left" | "right";
    }>;
    parseValue: import('vue').ComputedRef<any>;
    toggleExpandCode: () => void;
}, {}, {}, {}, import('vue').ComponentOptionsMixin, import('vue').ComponentOptionsMixin, ("onKeyClick" | "copied")[], "onKeyClick" | "copied", import('vue').PublicProps, Readonly<{
    value: any;
    expanded?: boolean | undefined;
    expandDepth?: number | undefined;
    copyable?: (boolean | CopyableOptions) | undefined;
    sort?: boolean | undefined;
    boxed?: boolean | undefined;
    theme?: string | undefined;
    timeformat?: ((value: Date) => string) | undefined;
    previewMode?: boolean | undefined;
    parse?: boolean | undefined;
}> & Readonly<{
    onOnKeyClick?: ((...args: any[]) => any) | undefined;
    onCopied?: ((...args: any[]) => any) | undefined;
}>, {
    sort: boolean | undefined;
    previewMode: boolean | undefined;
    timeformat: ((value: Date) => string) | undefined;
    expandDepth: number | undefined;
    expanded: boolean | undefined;
    copyable: boolean | CopyableOptions | undefined;
    boxed: boolean | undefined;
    theme: string | undefined;
    parse: boolean | undefined;
}, {}, {
    JsonBox: import('vue').DefineComponent<import('vue').ExtractPropTypes<{
        value: {
            type: PropType<any>;
            default: null;
        };
        keyName: {
            type: StringConstructor;
            default: string;
        };
        sort: BooleanConstructor;
        depth: {
            type: NumberConstructor;
            default: number;
        };
        previewMode: BooleanConstructor;
    }>, () => import('vue').VNode<import('vue').RendererNode, import('vue').RendererElement, {
        [key: string]: any;
    }>, {}, {}, {}, import('vue').ComponentOptionsMixin, import('vue').ComponentOptionsMixin, {}, string, import('vue').PublicProps, Readonly<import('vue').ExtractPropTypes<{
        value: {
            type: PropType<any>;
            default: null;
        };
        keyName: {
            type: StringConstructor;
            default: string;
        };
        sort: BooleanConstructor;
        depth: {
            type: NumberConstructor;
            default: number;
        };
        previewMode: BooleanConstructor;
    }>> & Readonly<{}>, {
        sort: boolean;
        previewMode: boolean;
        keyName: string;
        depth: number;
        value: any;
    }, {}, {}, {}, string, import('vue').ComponentProvideOptions, true, {}, any>;
}, {}, string, import('vue').ComponentProvideOptions, true, {}, any>;
export default _default;
