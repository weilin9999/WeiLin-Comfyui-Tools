import { PropType, VNode } from 'vue';
/**
 * JsonBox is a recursive component used by JsonViewer to render individual
 * JSON properties (key-value pairs) or array items. It determines the data type
 * of the value and delegates rendering to a type-specific component.
 */
declare const _default: import('vue').DefineComponent<import('vue').ExtractPropTypes<{
    /** The JSON value to render. Can be any valid JSON type. */
    value: {
        type: PropType<any>;
        default: null;
    };
    /** The key name for this value, if it's part of an object. */
    keyName: {
        type: StringConstructor;
        default: string;
    };
    /** Whether to sort object keys alphabetically. Passed down from JsonViewer. */
    sort: BooleanConstructor;
    /** Current nesting depth of this component. */
    depth: {
        type: NumberConstructor;
        default: number;
    };
    /** Whether preview mode is enabled. Passed down from JsonViewer. */
    previewMode: BooleanConstructor;
}>, () => VNode<import('vue').RendererNode, import('vue').RendererElement, {
    [key: string]: any;
}>, {}, {}, {}, import('vue').ComponentOptionsMixin, import('vue').ComponentOptionsMixin, {}, string, import('vue').PublicProps, Readonly<import('vue').ExtractPropTypes<{
    /** The JSON value to render. Can be any valid JSON type. */
    value: {
        type: PropType<any>;
        default: null;
    };
    /** The key name for this value, if it's part of an object. */
    keyName: {
        type: StringConstructor;
        default: string;
    };
    /** Whether to sort object keys alphabetically. Passed down from JsonViewer. */
    sort: BooleanConstructor;
    /** Current nesting depth of this component. */
    depth: {
        type: NumberConstructor;
        default: number;
    };
    /** Whether preview mode is enabled. Passed down from JsonViewer. */
    previewMode: BooleanConstructor;
}>> & Readonly<{}>, {
    sort: boolean;
    previewMode: boolean;
    keyName: string;
    depth: number;
    value: any;
}, {}, {}, {}, string, import('vue').ComponentProvideOptions, true, {}, any>;
export default _default;
