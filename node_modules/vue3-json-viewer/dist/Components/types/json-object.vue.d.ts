import { PropType, VNode } from 'vue';
/**
 * JsonObject component renders JSON objects. It can be expanded or collapsed,
 * sort its keys, and recursively renders its properties using JsonBox.
 */
declare const _default: import('vue').DefineComponent<import('vue').ExtractPropTypes<{
    /** The object value to render. */
    jsonValue: {
        type: PropType<Record<string, any>>;
        required: true;
    };
    /** The key name of this object if it's a property of another object. */
    keyName: {
        type: StringConstructor;
        default: string;
    };
    /** Current nesting depth of this object. */
    depth: {
        type: NumberConstructor;
        default: number;
    };
    /** Whether this object should be rendered in an expanded state. */
    expand: BooleanConstructor;
    /** Whether to sort the keys of this object alphabetically. */
    sort: BooleanConstructor;
    /** Whether preview mode is enabled. */
    previewMode: BooleanConstructor;
}>, () => VNode<import('vue').RendererNode, import('vue').RendererElement, {
    [key: string]: any;
}>, {}, {}, {}, import('vue').ComponentOptionsMixin, import('vue').ComponentOptionsMixin, "update:expand"[], "update:expand", import('vue').PublicProps, Readonly<import('vue').ExtractPropTypes<{
    /** The object value to render. */
    jsonValue: {
        type: PropType<Record<string, any>>;
        required: true;
    };
    /** The key name of this object if it's a property of another object. */
    keyName: {
        type: StringConstructor;
        default: string;
    };
    /** Current nesting depth of this object. */
    depth: {
        type: NumberConstructor;
        default: number;
    };
    /** Whether this object should be rendered in an expanded state. */
    expand: BooleanConstructor;
    /** Whether to sort the keys of this object alphabetically. */
    sort: BooleanConstructor;
    /** Whether preview mode is enabled. */
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
