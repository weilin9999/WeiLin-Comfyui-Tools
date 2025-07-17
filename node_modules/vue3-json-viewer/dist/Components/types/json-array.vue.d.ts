import { PropType, VNode } from 'vue';
/**
 * JsonArray component renders JSON arrays. It can be expanded or collapsed
 * and recursively renders its items using JsonBox.
 */
declare const _default: import('vue').DefineComponent<import('vue').ExtractPropTypes<{
    /** The array value to render. */
    jsonValue: {
        type: PropType<any[]>;
        required: true;
    };
    /** The key name of this array if it's a property of an object. */
    keyName: {
        type: StringConstructor;
        default: string;
    };
    /** Current nesting depth of this array. */
    depth: {
        type: NumberConstructor;
        default: number;
    };
    /** Whether to sort array items (Note: arrays are typically not sorted by key). */
    sort: BooleanConstructor;
    /** Whether this array should be rendered in an expanded state. */
    expand: BooleanConstructor;
    /** Whether preview mode is enabled (potentially showing a condensed view). */
    previewMode: BooleanConstructor;
}>, () => VNode<import('vue').RendererNode, import('vue').RendererElement, {
    [key: string]: any;
}>, {}, {}, {}, import('vue').ComponentOptionsMixin, import('vue').ComponentOptionsMixin, "update:expand"[], "update:expand", import('vue').PublicProps, Readonly<import('vue').ExtractPropTypes<{
    /** The array value to render. */
    jsonValue: {
        type: PropType<any[]>;
        required: true;
    };
    /** The key name of this array if it's a property of an object. */
    keyName: {
        type: StringConstructor;
        default: string;
    };
    /** Current nesting depth of this array. */
    depth: {
        type: NumberConstructor;
        default: number;
    };
    /** Whether to sort array items (Note: arrays are typically not sorted by key). */
    sort: BooleanConstructor;
    /** Whether this array should be rendered in an expanded state. */
    expand: BooleanConstructor;
    /** Whether preview mode is enabled (potentially showing a condensed view). */
    previewMode: BooleanConstructor;
}>> & Readonly<{
    "onUpdate:expand"?: ((...args: any[]) => any) | undefined;
}>, {
    sort: boolean;
    expand: boolean;
    previewMode: boolean;
    keyName: string;
    depth: number;
}, {}, {}, {}, string, import('vue').ComponentProvideOptions, true, {}, any>;
export default _default;
