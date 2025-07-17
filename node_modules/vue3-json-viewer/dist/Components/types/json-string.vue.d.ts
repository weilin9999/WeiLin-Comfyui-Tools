import { PropType, VNode } from 'vue';
/**
 * JsonString component renders JSON string values.
 * It supports expanding/collapsing long strings and automatically creates hyperlinks for URLs.
 */
declare const _default: import('vue').DefineComponent<import('vue').ExtractPropTypes<{
    /** The string value to display. */
    jsonValue: {
        type: PropType<string>;
        required: true;
    };
}>, () => VNode<import('vue').RendererNode, import('vue').RendererElement, {
    [key: string]: any;
}>, {}, {}, {}, import('vue').ComponentOptionsMixin, import('vue').ComponentOptionsMixin, {}, string, import('vue').PublicProps, Readonly<import('vue').ExtractPropTypes<{
    /** The string value to display. */
    jsonValue: {
        type: PropType<string>;
        required: true;
    };
}>> & Readonly<{}>, {}, {}, {}, {}, string, import('vue').ComponentProvideOptions, true, {}, any>;
export default _default;
