--
-- PostgreSQL database dump
--

-- Dumped from database version 16.9 (84ade85)
-- Dumped by pg_dump version 16.9

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: access_controls; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.access_controls (
    id integer NOT NULL,
    user_id integer NOT NULL,
    control_type character varying(50) NOT NULL,
    control_value character varying(500) NOT NULL,
    is_active boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.access_controls OWNER TO neondb_owner;

--
-- Name: access_controls_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.access_controls_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.access_controls_id_seq OWNER TO neondb_owner;

--
-- Name: access_controls_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.access_controls_id_seq OWNED BY public.access_controls.id;


--
-- Name: ad_entities; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.ad_entities (
    id integer NOT NULL,
    user_id integer NOT NULL,
    platform character varying(50) NOT NULL,
    campaign_id character varying(100),
    adset_id character varying(100),
    ad_id character varying(100),
    objective character varying(50),
    budget_daily double precision,
    status character varying(20),
    created_at timestamp without time zone
);


ALTER TABLE public.ad_entities OWNER TO neondb_owner;

--
-- Name: ad_entities_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.ad_entities_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ad_entities_id_seq OWNER TO neondb_owner;

--
-- Name: ad_entities_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.ad_entities_id_seq OWNED BY public.ad_entities.id;


--
-- Name: agent_memory; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.agent_memory (
    id integer NOT NULL,
    user_id integer NOT NULL,
    key character varying(120),
    value text,
    created_at timestamp without time zone
);


ALTER TABLE public.agent_memory OWNER TO neondb_owner;

--
-- Name: agent_memory_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.agent_memory_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.agent_memory_id_seq OWNER TO neondb_owner;

--
-- Name: agent_memory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.agent_memory_id_seq OWNED BY public.agent_memory.id;


--
-- Name: ai_event; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.ai_event (
    id integer NOT NULL,
    user_id integer NOT NULL,
    event_type character varying(80),
    event_json text,
    success boolean,
    created_at timestamp without time zone
);


ALTER TABLE public.ai_event OWNER TO neondb_owner;

--
-- Name: ai_event_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.ai_event_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.ai_event_id_seq OWNER TO neondb_owner;

--
-- Name: ai_event_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.ai_event_id_seq OWNED BY public.ai_event.id;


--
-- Name: api_endpoint; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.api_endpoint (
    id integer NOT NULL,
    user_id integer NOT NULL,
    endpoint character varying(200) NOT NULL,
    method character varying(10),
    response_time double precision,
    status_code integer,
    error_message text,
    created_at timestamp without time zone
);


ALTER TABLE public.api_endpoint OWNER TO neondb_owner;

--
-- Name: api_endpoint_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.api_endpoint_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_endpoint_id_seq OWNER TO neondb_owner;

--
-- Name: api_endpoint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.api_endpoint_id_seq OWNED BY public.api_endpoint.id;


--
-- Name: api_endpoints; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.api_endpoints (
    id integer NOT NULL,
    user_id integer NOT NULL,
    endpoint_name character varying(100) NOT NULL,
    url character varying(500) NOT NULL,
    method character varying(10) NOT NULL,
    headers text,
    payload text,
    created_at timestamp without time zone,
    last_used timestamp without time zone,
    usage_count integer
);


ALTER TABLE public.api_endpoints OWNER TO neondb_owner;

--
-- Name: api_endpoints_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.api_endpoints_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.api_endpoints_id_seq OWNER TO neondb_owner;

--
-- Name: api_endpoints_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.api_endpoints_id_seq OWNED BY public.api_endpoints.id;


--
-- Name: audit_logs; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.audit_logs (
    id integer NOT NULL,
    tenant_id integer NOT NULL,
    actor character varying(100) NOT NULL,
    action character varying(100) NOT NULL,
    payload_json text,
    ip_address character varying(45),
    user_agent character varying(500),
    created_at timestamp without time zone
);


ALTER TABLE public.audit_logs OWNER TO neondb_owner;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.audit_logs_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.audit_logs_id_seq OWNER TO neondb_owner;

--
-- Name: audit_logs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.audit_logs_id_seq OWNED BY public.audit_logs.id;


--
-- Name: connected_stores; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.connected_stores (
    id integer NOT NULL,
    user_id integer NOT NULL,
    platform character varying(50) NOT NULL,
    store_url character varying(500) NOT NULL,
    current_revenue integer,
    status character varying(50),
    api_credentials text,
    last_sync timestamp without time zone,
    connected_at timestamp without time zone
);


ALTER TABLE public.connected_stores OWNER TO neondb_owner;

--
-- Name: connected_stores_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.connected_stores_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.connected_stores_id_seq OWNER TO neondb_owner;

--
-- Name: connected_stores_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.connected_stores_id_seq OWNED BY public.connected_stores.id;


--
-- Name: integrations; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.integrations (
    id integer NOT NULL,
    code character varying(50) NOT NULL,
    display_name character varying(100) NOT NULL,
    auth_type character varying(20) NOT NULL,
    description text,
    icon_class character varying(100),
    created_at timestamp without time zone
);


ALTER TABLE public.integrations OWNER TO neondb_owner;

--
-- Name: integrations_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.integrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.integrations_id_seq OWNER TO neondb_owner;

--
-- Name: integrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.integrations_id_seq OWNED BY public.integrations.id;


--
-- Name: invite_codes; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.invite_codes (
    id integer NOT NULL,
    code character varying(32) NOT NULL,
    created_by integer NOT NULL,
    used_by integer,
    uses_remaining integer,
    expires_at timestamp without time zone,
    is_active boolean,
    created_at timestamp without time zone,
    used_at timestamp without time zone
);


ALTER TABLE public.invite_codes OWNER TO neondb_owner;

--
-- Name: invite_codes_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.invite_codes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.invite_codes_id_seq OWNER TO neondb_owner;

--
-- Name: invite_codes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.invite_codes_id_seq OWNED BY public.invite_codes.id;


--
-- Name: plugin; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.plugin (
    id integer NOT NULL,
    owner_id integer NOT NULL,
    name character varying(120) NOT NULL,
    description text,
    code_blob text,
    created_at timestamp without time zone
);


ALTER TABLE public.plugin OWNER TO neondb_owner;

--
-- Name: plugin_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.plugin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.plugin_id_seq OWNER TO neondb_owner;

--
-- Name: plugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.plugin_id_seq OWNED BY public.plugin.id;


--
-- Name: product_store; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.product_store (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    price double precision,
    category character varying(100),
    file_path character varying(500),
    shopify_product_id character varying(120),
    status character varying(50),
    revenue double precision,
    created_at timestamp without time zone
);


ALTER TABLE public.product_store OWNER TO neondb_owner;

--
-- Name: product_store_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.product_store_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.product_store_id_seq OWNER TO neondb_owner;

--
-- Name: product_store_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.product_store_id_seq OWNED BY public.product_store.id;


--
-- Name: profit_log; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.profit_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    source character varying(100) NOT NULL,
    amount double precision NOT NULL,
    profit_type character varying(50),
    date date,
    additional_metadata text,
    created_at timestamp without time zone
);


ALTER TABLE public.profit_log OWNER TO neondb_owner;

--
-- Name: profit_log_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.profit_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.profit_log_id_seq OWNER TO neondb_owner;

--
-- Name: profit_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.profit_log_id_seq OWNED BY public.profit_log.id;


--
-- Name: shopify_order; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.shopify_order (
    id integer NOT NULL,
    user_id integer NOT NULL,
    shopify_order_id character varying(120),
    total_price double precision,
    currency character varying(8),
    status character varying(32),
    created_at timestamp without time zone
);


ALTER TABLE public.shopify_order OWNER TO neondb_owner;

--
-- Name: shopify_order_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.shopify_order_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.shopify_order_id_seq OWNER TO neondb_owner;

--
-- Name: shopify_order_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.shopify_order_id_seq OWNED BY public.shopify_order.id;


--
-- Name: social_posts; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.social_posts (
    id integer NOT NULL,
    user_id integer NOT NULL,
    platform character varying(50) NOT NULL,
    post_id character varying(100) NOT NULL,
    status character varying(20),
    caption text,
    media_url character varying(500),
    link_url character varying(500),
    created_at timestamp without time zone
);


ALTER TABLE public.social_posts OWNER TO neondb_owner;

--
-- Name: social_posts_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.social_posts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.social_posts_id_seq OWNER TO neondb_owner;

--
-- Name: social_posts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.social_posts_id_seq OWNED BY public.social_posts.id;


--
-- Name: strategy_cache; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.strategy_cache (
    id integer NOT NULL,
    user_id integer NOT NULL,
    strategy character varying(200) NOT NULL,
    average_profit double precision,
    usage_count integer,
    success_rate double precision,
    last_used timestamp without time zone,
    performance_data text,
    created_at timestamp without time zone
);


ALTER TABLE public.strategy_cache OWNER TO neondb_owner;

--
-- Name: strategy_cache_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.strategy_cache_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.strategy_cache_id_seq OWNER TO neondb_owner;

--
-- Name: strategy_cache_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.strategy_cache_id_seq OWNED BY public.strategy_cache.id;


--
-- Name: subscription; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.subscription (
    id integer NOT NULL,
    user_id integer NOT NULL,
    stripe_customer_id character varying(120),
    stripe_subscription_id character varying(120),
    plan_id character varying(64),
    status character varying(64),
    current_period_end integer,
    created_at timestamp without time zone
);


ALTER TABLE public.subscription OWNER TO neondb_owner;

--
-- Name: subscription_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.subscription_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.subscription_id_seq OWNER TO neondb_owner;

--
-- Name: subscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.subscription_id_seq OWNED BY public.subscription.id;


--
-- Name: team; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.team (
    id integer NOT NULL,
    owner_id integer NOT NULL,
    name character varying(120) NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.team OWNER TO neondb_owner;

--
-- Name: team_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.team_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.team_id_seq OWNER TO neondb_owner;

--
-- Name: team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.team_id_seq OWNED BY public.team.id;


--
-- Name: team_member; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.team_member (
    id integer NOT NULL,
    team_id integer NOT NULL,
    user_id integer NOT NULL,
    role character varying(32),
    created_at timestamp without time zone
);


ALTER TABLE public.team_member OWNER TO neondb_owner;

--
-- Name: team_member_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.team_member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.team_member_id_seq OWNER TO neondb_owner;

--
-- Name: team_member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.team_member_id_seq OWNED BY public.team_member.id;


--
-- Name: tenant_connections; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tenant_connections (
    id integer NOT NULL,
    tenant_id integer NOT NULL,
    integration_code character varying(50) NOT NULL,
    status character varying(50),
    meta_json text,
    created_at timestamp without time zone,
    updated_at timestamp without time zone
);


ALTER TABLE public.tenant_connections OWNER TO neondb_owner;

--
-- Name: tenant_connections_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tenant_connections_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tenant_connections_id_seq OWNER TO neondb_owner;

--
-- Name: tenant_connections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tenant_connections_id_seq OWNED BY public.tenant_connections.id;


--
-- Name: tenant_secrets; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tenant_secrets (
    id integer NOT NULL,
    connection_id integer NOT NULL,
    key character varying(100) NOT NULL,
    value_encrypted text NOT NULL,
    created_at timestamp without time zone
);


ALTER TABLE public.tenant_secrets OWNER TO neondb_owner;

--
-- Name: tenant_secrets_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tenant_secrets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tenant_secrets_id_seq OWNER TO neondb_owner;

--
-- Name: tenant_secrets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tenant_secrets_id_seq OWNED BY public.tenant_secrets.id;


--
-- Name: tenants; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.tenants (
    id integer NOT NULL,
    owner_user_id integer NOT NULL,
    stripe_customer_id character varying(120),
    stripe_subscription_id character varying(120),
    stripe_connect_account_id character varying(120),
    plan character varying(50),
    status character varying(50),
    created_at timestamp without time zone,
    autopilot_enabled boolean DEFAULT false
);


ALTER TABLE public.tenants OWNER TO neondb_owner;

--
-- Name: tenants_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.tenants_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tenants_id_seq OWNER TO neondb_owner;

--
-- Name: tenants_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.tenants_id_seq OWNED BY public.tenants.id;


--
-- Name: trend_data; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.trend_data (
    id integer NOT NULL,
    source character varying(100) NOT NULL,
    keyword character varying(200) NOT NULL,
    rank integer,
    trend_score double precision,
    category character varying(100),
    additional_data text,
    "timestamp" timestamp without time zone
);


ALTER TABLE public.trend_data OWNER TO neondb_owner;

--
-- Name: trend_data_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.trend_data_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.trend_data_id_seq OWNER TO neondb_owner;

--
-- Name: trend_data_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.trend_data_id_seq OWNED BY public.trend_data.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(80),
    email character varying(120) NOT NULL,
    password_hash character varying(255) NOT NULL,
    stripe_customer_id character varying(255),
    subscription_status character varying(50),
    created_at timestamp without time zone,
    voice_name character varying(100),
    voice_personality character varying(50),
    voice_enabled boolean,
    voice_type character varying(50),
    role character varying(50)
);


ALTER TABLE public."user" OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_id_seq OWNER TO neondb_owner;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: user_plugin; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.user_plugin (
    id integer NOT NULL,
    user_id integer NOT NULL,
    plugin_id integer NOT NULL,
    installed_at timestamp without time zone
);


ALTER TABLE public.user_plugin OWNER TO neondb_owner;

--
-- Name: user_plugin_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_plugin_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_plugin_id_seq OWNER TO neondb_owner;

--
-- Name: user_plugin_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_plugin_id_seq OWNED BY public.user_plugin.id;


--
-- Name: user_preferences; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.user_preferences (
    id integer NOT NULL,
    user_id integer NOT NULL,
    voice_enabled boolean DEFAULT false,
    agent_name text DEFAULT 'AI CEO'::text,
    personality text DEFAULT 'professional'::text,
    voice_type text DEFAULT 'professional'::text,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.user_preferences OWNER TO neondb_owner;

--
-- Name: user_preferences_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_preferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_preferences_id_seq OWNER TO neondb_owner;

--
-- Name: user_preferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_preferences_id_seq OWNED BY public.user_preferences.id;


--
-- Name: user_settings; Type: TABLE; Schema: public; Owner: neondb_owner
--

CREATE TABLE public.user_settings (
    id integer NOT NULL,
    user_id integer NOT NULL,
    logo_path character varying(256),
    primary_color character varying(16),
    secondary_color character varying(16),
    subdomain character varying(120),
    created_at timestamp without time zone
);


ALTER TABLE public.user_settings OWNER TO neondb_owner;

--
-- Name: user_settings_id_seq; Type: SEQUENCE; Schema: public; Owner: neondb_owner
--

CREATE SEQUENCE public.user_settings_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.user_settings_id_seq OWNER TO neondb_owner;

--
-- Name: user_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: neondb_owner
--

ALTER SEQUENCE public.user_settings_id_seq OWNED BY public.user_settings.id;


--
-- Name: access_controls id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.access_controls ALTER COLUMN id SET DEFAULT nextval('public.access_controls_id_seq'::regclass);


--
-- Name: ad_entities id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ad_entities ALTER COLUMN id SET DEFAULT nextval('public.ad_entities_id_seq'::regclass);


--
-- Name: agent_memory id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.agent_memory ALTER COLUMN id SET DEFAULT nextval('public.agent_memory_id_seq'::regclass);


--
-- Name: ai_event id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ai_event ALTER COLUMN id SET DEFAULT nextval('public.ai_event_id_seq'::regclass);


--
-- Name: api_endpoint id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.api_endpoint ALTER COLUMN id SET DEFAULT nextval('public.api_endpoint_id_seq'::regclass);


--
-- Name: api_endpoints id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.api_endpoints ALTER COLUMN id SET DEFAULT nextval('public.api_endpoints_id_seq'::regclass);


--
-- Name: audit_logs id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.audit_logs ALTER COLUMN id SET DEFAULT nextval('public.audit_logs_id_seq'::regclass);


--
-- Name: connected_stores id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.connected_stores ALTER COLUMN id SET DEFAULT nextval('public.connected_stores_id_seq'::regclass);


--
-- Name: integrations id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.integrations ALTER COLUMN id SET DEFAULT nextval('public.integrations_id_seq'::regclass);


--
-- Name: invite_codes id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.invite_codes ALTER COLUMN id SET DEFAULT nextval('public.invite_codes_id_seq'::regclass);


--
-- Name: plugin id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.plugin ALTER COLUMN id SET DEFAULT nextval('public.plugin_id_seq'::regclass);


--
-- Name: product_store id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.product_store ALTER COLUMN id SET DEFAULT nextval('public.product_store_id_seq'::regclass);


--
-- Name: profit_log id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.profit_log ALTER COLUMN id SET DEFAULT nextval('public.profit_log_id_seq'::regclass);


--
-- Name: shopify_order id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.shopify_order ALTER COLUMN id SET DEFAULT nextval('public.shopify_order_id_seq'::regclass);


--
-- Name: social_posts id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.social_posts ALTER COLUMN id SET DEFAULT nextval('public.social_posts_id_seq'::regclass);


--
-- Name: strategy_cache id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.strategy_cache ALTER COLUMN id SET DEFAULT nextval('public.strategy_cache_id_seq'::regclass);


--
-- Name: subscription id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.subscription ALTER COLUMN id SET DEFAULT nextval('public.subscription_id_seq'::regclass);


--
-- Name: team id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team ALTER COLUMN id SET DEFAULT nextval('public.team_id_seq'::regclass);


--
-- Name: team_member id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_member ALTER COLUMN id SET DEFAULT nextval('public.team_member_id_seq'::regclass);


--
-- Name: tenant_connections id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenant_connections ALTER COLUMN id SET DEFAULT nextval('public.tenant_connections_id_seq'::regclass);


--
-- Name: tenant_secrets id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenant_secrets ALTER COLUMN id SET DEFAULT nextval('public.tenant_secrets_id_seq'::regclass);


--
-- Name: tenants id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenants ALTER COLUMN id SET DEFAULT nextval('public.tenants_id_seq'::regclass);


--
-- Name: trend_data id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.trend_data ALTER COLUMN id SET DEFAULT nextval('public.trend_data_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: user_plugin id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_plugin ALTER COLUMN id SET DEFAULT nextval('public.user_plugin_id_seq'::regclass);


--
-- Name: user_preferences id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_preferences ALTER COLUMN id SET DEFAULT nextval('public.user_preferences_id_seq'::regclass);


--
-- Name: user_settings id; Type: DEFAULT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_settings ALTER COLUMN id SET DEFAULT nextval('public.user_settings_id_seq'::regclass);


--
-- Data for Name: access_controls; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.access_controls (id, user_id, control_type, control_value, is_active, created_at) FROM stdin;
\.


--
-- Data for Name: ad_entities; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.ad_entities (id, user_id, platform, campaign_id, adset_id, ad_id, objective, budget_daily, status, created_at) FROM stdin;
\.


--
-- Data for Name: agent_memory; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.agent_memory (id, user_id, key, value, created_at) FROM stdin;
\.


--
-- Data for Name: ai_event; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.ai_event (id, user_id, event_type, event_json, success, created_at) FROM stdin;
1	2	one_click_start	{"niche": "digital marketing", "target_audience": "entrepreneurs", "start_time": "2025-08-27T20:28:58.512126"}	t	2025-08-27 20:28:58.512163
2	2	product_created	{"product_name": "The Ultimate Digital Marketing Blueprint", "price": 97, "type": "ebook", "niche": "digital marketing"}	t	2025-08-27 20:29:03.849715
3	2	product_created	{"product_name": "Facebook Ads Mastery Course", "price": 197, "type": "course", "niche": "digital marketing"}	t	2025-08-27 20:29:04.5049
4	2	product_created	{"product_name": "Email Marketing Automation Software", "price": 297, "type": "software", "niche": "digital marketing"}	t	2025-08-27 20:29:05.156413
5	2	one_click_complete	{"niche": "digital marketing", "products_count": 3, "marketing_assets": 3, "elapsed_seconds": 29.87581, "success": true}	t	2025-08-27 20:29:28.388006
7	2	agent_command	{"command": "Analyze competitor strategies in [market]", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:32:38.425514
6	2	agent_command	{"command": "Analyze competitor strategies in [market]", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:32:38.419735
8	2	agent_command	{"command": "Analyze competitor strategies in [market]", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:32:39.89542
9	2	agent_command	{"command": "Analyze competitor strategies in [market]", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:32:39.898143
10	2	agent_command	{"command": "Analyze competitor strategies in [market]", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:33:18.758355
11	2	agent_command	{"command": "Analyze competitor strategies in [market]", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:33:18.839168
12	2	agent_command	{"command": "Start autonomous profit-generation mode", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:33:33.831444
13	2	agent_command	{"command": "Start autonomous profit-generation mode", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:33:34.070117
14	2	agent_command	{"command": "Build sales funnel for maximum conversions", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:33:56.320911
15	2	agent_command	{"command": "Build sales funnel for maximum conversions", "voice_enabled": true, "name_learned": null}	t	2025-08-27 20:33:56.468557
16	2	agent_command	{"command": "Create [product type] with full documentation", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:29:48.956632
17	2	agent_command	{"command": "Create [product type] with full documentation", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:29:49.095461
18	2	one_click_start	{"niche": "e-commerce", "target_audience": "stay-at-home parents", "start_time": "2025-08-28T11:31:19.953040"}	t	2025-08-28 11:31:19.953069
19	2	product_created	{"product_name": "Parenting Hacks Ebook Bundle", "price": 25, "type": "ebook", "niche": "e-commerce"}	t	2025-08-28 11:31:27.002953
20	2	product_created	{"product_name": "Meal Planning Course for Busy Parents", "price": 49, "type": "course", "niche": "e-commerce"}	t	2025-08-28 11:31:27.663004
21	2	product_created	{"product_name": "Home Budgeting Template Bundle", "price": 29, "type": "template", "niche": "e-commerce"}	t	2025-08-28 11:31:28.321449
22	2	one_click_complete	{"niche": "e-commerce", "products_count": 3, "marketing_assets": 3, "elapsed_seconds": 35.021574, "success": true}	t	2025-08-28 11:31:54.974698
23	2	agent_command	{"command": "Generate AI-powered content strategy", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:19.138473
24	2	agent_command	{"command": "Generate AI-powered content strategy", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:19.167041
25	2	agent_command	{"command": "Use machine learning to predict profitable trends", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:20.856105
26	2	agent_command	{"command": "Use machine learning to predict profitable trends", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:20.864047
27	2	agent_command	{"command": "Optimize entire business using AI recommendations", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:22.970208
28	2	agent_command	{"command": "Optimize entire business using AI recommendations", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:22.972718
29	2	agent_command	{"command": "Analyze customer behavior patterns", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:24.939677
30	2	agent_command	{"command": "Analyze customer behavior patterns", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:24.940533
31	2	agent_command	{"command": "Analyze customer behavior patterns", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:37.893522
32	2	agent_command	{"command": "Analyze customer behavior patterns", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:38.044811
33	2	agent_command	{"command": "Analyze performance and suggest optimizations", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:40.638331
34	2	agent_command	{"command": "Analyze performance and suggest optimizations", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:40.639369
35	2	agent_command	{"command": "Start autonomous profit-generation mode", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:42.89379
36	2	agent_command	{"command": "Start autonomous profit-generation mode", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:42.894748
37	2	agent_command	{"command": "Set up automated customer service responses", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:44.694096
38	2	agent_command	{"command": "Set up automated customer service responses", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:44.695672
39	2	agent_command	{"command": "Schedule social media posts for the week", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:46.482166
40	2	agent_command	{"command": "Schedule social media posts for the week", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:46.483927
41	2	agent_command	{"command": "Optimize store SEO and search rankings", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:50.666617
42	2	agent_command	{"command": "Optimize store SEO and search rankings", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:50.671035
43	2	agent_command	{"command": "Create product collections and navigation menu", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:54.685793
44	2	agent_command	{"command": "Create product collections and navigation menu", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:54.693288
45	2	agent_command	{"command": "Design complete store layout for [niche] in modern style", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:57.440835
46	2	agent_command	{"command": "Design complete store layout for [niche] in modern style", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:33:57.4482
47	2	agent_command	{"command": "Update store branding and description", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:00.504406
48	2	agent_command	{"command": "Update store branding and description", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:00.510385
49	2	agent_command	{"command": "Setup store policies and legal pages", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:02.942928
50	2	agent_command	{"command": "Setup store policies and legal pages", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:03.136692
51	2	agent_command	{"command": "Customize store theme colors and branding for [niche]", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:05.111949
54	2	agent_command	{"command": "Create upsell and cross-sell products", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:07.106454
56	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:10.928967
57	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:11.050238
62	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:12.351184
64	2	agent_command	{"command": "Upload product to Shopify with SEO optimization", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:15.870595
68	2	agent_command	{"command": "Generate Facebook ad copy for [target audience]", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:25.757295
70	2	agent_command	{"command": "Create email marketing sequence for [product]", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:29.259257
52	2	agent_command	{"command": "Customize store theme colors and branding for [niche]", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:05.125924
53	2	agent_command	{"command": "Create upsell and cross-sell products", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:07.103009
55	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:10.901277
61	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:12.349339
67	2	agent_command	{"command": "Generate Facebook ad copy for [target audience]", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:25.755493
58	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:11.059001
59	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:11.283709
60	2	agent_command	{"command": "Generate product description that converts", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:11.304126
63	2	agent_command	{"command": "Upload product to Shopify with SEO optimization", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:15.867075
65	2	agent_command	{"command": "Optimize pricing strategy for higher profits", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:23.07993
66	2	agent_command	{"command": "Optimize pricing strategy for higher profits", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:23.08585
69	2	agent_command	{"command": "Create email marketing sequence for [product]", "voice_enabled": true, "name_learned": null}	t	2025-08-28 11:34:29.2542
71	2	agent_command	{"command": "Use machine learning to predict profitable trends", "result": "\\ud83d\\udcb0 AI CEO is optimizing revenue streams and analyzing profit maximization strategies..."}	t	2025-08-29 17:06:43.886202
72	2	agent_command	{"command": "Use machine learning to predict profitable trends", "result": "\\ud83d\\udcb0 AI CEO is optimizing revenue streams and analyzing profit maximization strategies..."}	t	2025-08-29 17:06:43.914012
73	5	agent_command_executed	{"command": "test AI", "timestamp": "2025-08-30T20:52:31.361902"}	t	2025-08-30 20:52:31.361937
74	5	agent_command_completed	{"command": "test AI", "result": "\\ud83e\\udd16 AI CEO is processing your command: 'test AI' - Implementation in progress...", "success": true}	t	2025-08-30 20:52:31.54115
75	5	one_click_start	{"niche": "tech gadgets", "target_audience": "entrepreneurs", "start_time": "2025-08-30T20:52:33.118477"}	t	2025-08-30 20:52:33.118504
76	5	product_created	{"product_name": "Tech Entrepreneur Bootcamp", "price": 197, "type": "course", "niche": "tech gadgets"}	t	2025-08-30 20:52:38.017798
77	5	product_created	{"product_name": "Ultimate Tech Gadgets Productivity Guide", "price": 25, "type": "ebook", "niche": "tech gadgets"}	t	2025-08-30 20:52:38.674901
78	5	product_created	{"product_name": "Tech Startup Financial Planning Template", "price": 49, "type": "template", "niche": "tech gadgets"}	t	2025-08-30 20:52:39.344896
79	5	one_click_complete	{"niche": "tech gadgets", "products_count": 3, "marketing_assets": 3, "elapsed_seconds": 26.641088, "success": true}	t	2025-08-30 20:52:59.759624
80	5	one_click_start	{"niche": "fitness", "target_audience": "entrepreneurs", "start_time": "2025-08-30T20:55:38.755942"}	t	2025-08-30 20:55:38.755978
81	5	product_created	{"product_name": "Fitpreneur Bootcamp", "price": 197, "type": "course", "niche": "fitness"}	t	2025-08-30 20:55:44.054189
82	5	product_created	{"product_name": "Entrepreneurial Desk Workout Guide", "price": 25, "type": "ebook", "niche": "fitness"}	t	2025-08-30 20:55:44.710351
83	5	product_created	{"product_name": "Fitpreneur Meal Prep Templates", "price": 37, "type": "template", "niche": "fitness"}	t	2025-08-30 20:55:45.361101
84	5	one_click_complete	{"niche": "fitness", "products_count": 3, "marketing_assets": 3, "elapsed_seconds": 28.520156, "success": true}	t	2025-08-30 20:56:07.276158
85	3	google_ads_campaign_created	{"product_name": "AI Business Generator", "campaign_id": null, "success": false, "daily_budget": null}	t	2025-08-31 12:29:48.301877
86	3	google_ads_campaign_created	{"product_name": "AI Business Generator", "campaign_id": null, "success": false, "daily_budget": null}	t	2025-08-31 12:30:15.311059
87	3	google_ads_campaign_created	{"product_name": "AI Business Generator", "campaign_id": null, "success": false, "daily_budget": null}	t	2025-08-31 12:30:39.888317
88	3	google_ads_campaign_created	{"product_name": "AI CEO Platform", "campaign_id": null, "success": false, "daily_budget": null}	t	2025-08-31 12:32:53.398862
89	3	youtube_campaign_created	{"product_name": "AI CEO Platform", "video_id": "sim_yt_5167590605309900001", "success": true, "simulation": true}	t	2025-08-31 14:12:59.651612
\.


--
-- Data for Name: api_endpoint; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.api_endpoint (id, user_id, endpoint, method, response_time, status_code, error_message, created_at) FROM stdin;
\.


--
-- Data for Name: api_endpoints; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.api_endpoints (id, user_id, endpoint_name, url, method, headers, payload, created_at, last_used, usage_count) FROM stdin;
\.


--
-- Data for Name: audit_logs; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.audit_logs (id, tenant_id, actor, action, payload_json, ip_address, user_agent, created_at) FROM stdin;
\.


--
-- Data for Name: connected_stores; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.connected_stores (id, user_id, platform, store_url, current_revenue, status, api_credentials, last_sync, connected_at) FROM stdin;
\.


--
-- Data for Name: integrations; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.integrations (id, code, display_name, auth_type, description, icon_class, created_at) FROM stdin;
1	shopify	Shopify	oauth	Connect your Shopify store for product management and order processing	fa-shopping-cart	2025-08-30 12:25:43.30011
2	google	Google/YouTube	oauth	Connect Google and YouTube for content publishing and ads	fa-google	2025-08-30 12:25:43.369278
3	meta	Meta (Facebook/Instagram)	oauth	Connect Facebook and Instagram for social media marketing	fa-facebook	2025-08-30 12:25:43.43201
4	linkedin	LinkedIn	oauth	Connect LinkedIn for professional content publishing	fa-linkedin	2025-08-30 12:25:43.495832
5	x	X (Twitter)	oauth	Connect X (Twitter) for social media engagement	fa-twitter	2025-08-30 12:25:43.559574
6	openrouter	OpenRouter AI	apikey	Use your own OpenRouter API key for AI content generation	fa-robot	2025-08-30 12:25:43.622256
\.


--
-- Data for Name: invite_codes; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.invite_codes (id, code, created_by, used_by, uses_remaining, expires_at, is_active, created_at, used_at) FROM stdin;
\.


--
-- Data for Name: plugin; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.plugin (id, owner_id, name, description, code_blob, created_at) FROM stdin;
\.


--
-- Data for Name: product_store; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.product_store (id, user_id, title, description, price, category, file_path, shopify_product_id, status, revenue, created_at) FROM stdin;
\.


--
-- Data for Name: profit_log; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.profit_log (id, user_id, source, amount, profit_type, date, additional_metadata, created_at) FROM stdin;
\.


--
-- Data for Name: shopify_order; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.shopify_order (id, user_id, shopify_order_id, total_price, currency, status, created_at) FROM stdin;
\.


--
-- Data for Name: social_posts; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.social_posts (id, user_id, platform, post_id, status, caption, media_url, link_url, created_at) FROM stdin;
\.


--
-- Data for Name: strategy_cache; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.strategy_cache (id, user_id, strategy, average_profit, usage_count, success_rate, last_used, performance_data, created_at) FROM stdin;
\.


--
-- Data for Name: subscription; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.subscription (id, user_id, stripe_customer_id, stripe_subscription_id, plan_id, status, current_period_end, created_at) FROM stdin;
\.


--
-- Data for Name: team; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.team (id, owner_id, name, created_at) FROM stdin;
\.


--
-- Data for Name: team_member; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.team_member (id, team_id, user_id, role, created_at) FROM stdin;
\.


--
-- Data for Name: tenant_connections; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tenant_connections (id, tenant_id, integration_code, status, meta_json, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: tenant_secrets; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tenant_secrets (id, connection_id, key, value_encrypted, created_at) FROM stdin;
\.


--
-- Data for Name: tenants; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.tenants (id, owner_user_id, stripe_customer_id, stripe_subscription_id, stripe_connect_account_id, plan, status, created_at, autopilot_enabled) FROM stdin;
3	3	\N	\N	\N	starter	active	2025-08-31 09:32:39.501286	t
\.


--
-- Data for Name: trend_data; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.trend_data (id, source, keyword, rank, trend_score, category, additional_data, "timestamp") FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public."user" (id, username, email, password_hash, stripe_customer_id, subscription_status, created_at, voice_name, voice_personality, voice_enabled, voice_type, role) FROM stdin;
1	admin	admin@example.com	scrypt:32768:8:1$Sc4eTV2HKKDBmNgE$bf25d6460849140dfaffba57d2d5e6aabc17ce324142c3e353ca8fd80e671c191022ef48e9cb815699a6cd3914b875c73590bcb201bdf3836bdd8aa957c17252	\N	trial	2025-08-25 11:48:53.041487	AI CEO	professional	t	professional	admin
2	\N	tylerstarks45@gmail.com	scrypt:32768:8:1$xOpUf5lzQCgC8yA6$7f87227d173d74d07b2fc5327560675a27dbdd05a03f126dce04d78576c5d4c5af78d93f233def5668f03f9dcc8b3ebe69f8d2577684b66e2b903a8c89c5e950	\N	trial	2025-08-25 12:52:05.978547	AI CEO	funny	t	professional	admin
3	\N	test@example.com	scrypt:32768:8:1$FNHJbWIC1dH8AVYP$a798f51f2315e9616e5dd7ad1af19eb18c6d2bf977bdc2d95e3bd3995546f2f91d1ff833379d4de94e4ef4c3864cbf52cc0eb43d09df32b80380ee1d3d1eefbb	\N	trial	2025-08-30 20:37:17.832001	AI CEO	professional	f	professional	user
4	\N	test2@example.com	scrypt:32768:8:1$PSyGA219Q1FkafAE$686fb9dcf0098aef693a10fef1cbaa633b476ae3532c7157c7d6bdb0b690478a58000fb515f03c2f5a99ce005d1d5a1578dbfe8952d12ec4cbf1f4edfc1a15ed	\N	trial	2025-08-30 20:37:28.157496	AI CEO	professional	f	professional	user
5	\N	tylerstarks77@gmail.com	scrypt:32768:8:1$WeI72ilYMuZzAx7F$537a027b111fa0775ac94d326376f9778e6205f0f3ac5131bc6ab3c401b0d2c749cdf708e2eefabf4212b87d83efa43e54b5ef4cfc44e77d9081363d5507ef69	\N	trial	2025-08-30 20:37:52.487363	AI CEO	professional	f	professional	user
\.


--
-- Data for Name: user_plugin; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.user_plugin (id, user_id, plugin_id, installed_at) FROM stdin;
\.


--
-- Data for Name: user_preferences; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.user_preferences (id, user_id, voice_enabled, agent_name, personality, voice_type, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: user_settings; Type: TABLE DATA; Schema: public; Owner: neondb_owner
--

COPY public.user_settings (id, user_id, logo_path, primary_color, secondary_color, subdomain, created_at) FROM stdin;
\.


--
-- Name: access_controls_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.access_controls_id_seq', 1, false);


--
-- Name: ad_entities_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.ad_entities_id_seq', 1, false);


--
-- Name: agent_memory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.agent_memory_id_seq', 1, false);


--
-- Name: ai_event_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.ai_event_id_seq', 89, true);


--
-- Name: api_endpoint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.api_endpoint_id_seq', 1, false);


--
-- Name: api_endpoints_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.api_endpoints_id_seq', 1, false);


--
-- Name: audit_logs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.audit_logs_id_seq', 1, false);


--
-- Name: connected_stores_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.connected_stores_id_seq', 1, false);


--
-- Name: integrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.integrations_id_seq', 6, true);


--
-- Name: invite_codes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.invite_codes_id_seq', 1, false);


--
-- Name: plugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.plugin_id_seq', 1, false);


--
-- Name: product_store_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.product_store_id_seq', 1, false);


--
-- Name: profit_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.profit_log_id_seq', 1, false);


--
-- Name: shopify_order_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.shopify_order_id_seq', 1, false);


--
-- Name: social_posts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.social_posts_id_seq', 1, false);


--
-- Name: strategy_cache_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.strategy_cache_id_seq', 1, false);


--
-- Name: subscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.subscription_id_seq', 1, false);


--
-- Name: team_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.team_id_seq', 1, false);


--
-- Name: team_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.team_member_id_seq', 1, false);


--
-- Name: tenant_connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tenant_connections_id_seq', 1, false);


--
-- Name: tenant_secrets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tenant_secrets_id_seq', 1, false);


--
-- Name: tenants_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.tenants_id_seq', 3, true);


--
-- Name: trend_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.trend_data_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_id_seq', 5, true);


--
-- Name: user_plugin_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_plugin_id_seq', 1, false);


--
-- Name: user_preferences_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_preferences_id_seq', 1, false);


--
-- Name: user_settings_id_seq; Type: SEQUENCE SET; Schema: public; Owner: neondb_owner
--

SELECT pg_catalog.setval('public.user_settings_id_seq', 1, false);


--
-- Name: access_controls access_controls_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.access_controls
    ADD CONSTRAINT access_controls_pkey PRIMARY KEY (id);


--
-- Name: ad_entities ad_entities_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ad_entities
    ADD CONSTRAINT ad_entities_pkey PRIMARY KEY (id);


--
-- Name: agent_memory agent_memory_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.agent_memory
    ADD CONSTRAINT agent_memory_pkey PRIMARY KEY (id);


--
-- Name: ai_event ai_event_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ai_event
    ADD CONSTRAINT ai_event_pkey PRIMARY KEY (id);


--
-- Name: api_endpoint api_endpoint_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.api_endpoint
    ADD CONSTRAINT api_endpoint_pkey PRIMARY KEY (id);


--
-- Name: api_endpoints api_endpoints_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.api_endpoints
    ADD CONSTRAINT api_endpoints_pkey PRIMARY KEY (id);


--
-- Name: audit_logs audit_logs_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_pkey PRIMARY KEY (id);


--
-- Name: connected_stores connected_stores_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.connected_stores
    ADD CONSTRAINT connected_stores_pkey PRIMARY KEY (id);


--
-- Name: integrations integrations_code_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.integrations
    ADD CONSTRAINT integrations_code_key UNIQUE (code);


--
-- Name: integrations integrations_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.integrations
    ADD CONSTRAINT integrations_pkey PRIMARY KEY (id);


--
-- Name: invite_codes invite_codes_code_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.invite_codes
    ADD CONSTRAINT invite_codes_code_key UNIQUE (code);


--
-- Name: invite_codes invite_codes_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.invite_codes
    ADD CONSTRAINT invite_codes_pkey PRIMARY KEY (id);


--
-- Name: plugin plugin_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.plugin
    ADD CONSTRAINT plugin_pkey PRIMARY KEY (id);


--
-- Name: product_store product_store_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.product_store
    ADD CONSTRAINT product_store_pkey PRIMARY KEY (id);


--
-- Name: profit_log profit_log_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.profit_log
    ADD CONSTRAINT profit_log_pkey PRIMARY KEY (id);


--
-- Name: shopify_order shopify_order_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.shopify_order
    ADD CONSTRAINT shopify_order_pkey PRIMARY KEY (id);


--
-- Name: shopify_order shopify_order_shopify_order_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.shopify_order
    ADD CONSTRAINT shopify_order_shopify_order_id_key UNIQUE (shopify_order_id);


--
-- Name: social_posts social_posts_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.social_posts
    ADD CONSTRAINT social_posts_pkey PRIMARY KEY (id);


--
-- Name: strategy_cache strategy_cache_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.strategy_cache
    ADD CONSTRAINT strategy_cache_pkey PRIMARY KEY (id);


--
-- Name: subscription subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT subscription_pkey PRIMARY KEY (id);


--
-- Name: team_member team_member_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_member
    ADD CONSTRAINT team_member_pkey PRIMARY KEY (id);


--
-- Name: team team_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_pkey PRIMARY KEY (id);


--
-- Name: tenant_connections tenant_connections_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenant_connections
    ADD CONSTRAINT tenant_connections_pkey PRIMARY KEY (id);


--
-- Name: tenant_secrets tenant_secrets_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenant_secrets
    ADD CONSTRAINT tenant_secrets_pkey PRIMARY KEY (id);


--
-- Name: tenants tenants_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_pkey PRIMARY KEY (id);


--
-- Name: trend_data trend_data_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.trend_data
    ADD CONSTRAINT trend_data_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_plugin user_plugin_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_plugin
    ADD CONSTRAINT user_plugin_pkey PRIMARY KEY (id);


--
-- Name: user_preferences user_preferences_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_pkey PRIMARY KEY (id);


--
-- Name: user_settings user_settings_pkey; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_pkey PRIMARY KEY (id);


--
-- Name: user_settings user_settings_user_id_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_user_id_key UNIQUE (user_id);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


--
-- Name: idx_access_controls_active; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_access_controls_active ON public.access_controls USING btree (is_active);


--
-- Name: idx_access_controls_user_type; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_access_controls_user_type ON public.access_controls USING btree (user_id, control_type);


--
-- Name: idx_ad_entities_user_platform; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_ad_entities_user_platform ON public.ad_entities USING btree (user_id, platform);


--
-- Name: idx_audit_logs_action; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_audit_logs_action ON public.audit_logs USING btree (action);


--
-- Name: idx_audit_logs_tenant_created; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_audit_logs_tenant_created ON public.audit_logs USING btree (tenant_id, created_at);


--
-- Name: idx_connected_stores_platform; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_connected_stores_platform ON public.connected_stores USING btree (platform);


--
-- Name: idx_connected_stores_user; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_connected_stores_user ON public.connected_stores USING btree (user_id);


--
-- Name: idx_invite_codes_active; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_invite_codes_active ON public.invite_codes USING btree (is_active);


--
-- Name: idx_invite_codes_code; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_invite_codes_code ON public.invite_codes USING btree (code);


--
-- Name: idx_profit_log_source; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_profit_log_source ON public.profit_log USING btree (source);


--
-- Name: idx_profit_log_user_date; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_profit_log_user_date ON public.profit_log USING btree (user_id, date);


--
-- Name: idx_social_posts_user_platform; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_social_posts_user_platform ON public.social_posts USING btree (user_id, platform);


--
-- Name: idx_strategy_cache_performance; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_strategy_cache_performance ON public.strategy_cache USING btree (average_profit, success_rate);


--
-- Name: idx_strategy_cache_user_strategy; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_strategy_cache_user_strategy ON public.strategy_cache USING btree (user_id, strategy);


--
-- Name: idx_tenant_connections_status; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_tenant_connections_status ON public.tenant_connections USING btree (status);


--
-- Name: idx_tenant_connections_tenant_integration; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_tenant_connections_tenant_integration ON public.tenant_connections USING btree (tenant_id, integration_code);


--
-- Name: idx_tenant_secrets_connection_key; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_tenant_secrets_connection_key ON public.tenant_secrets USING btree (connection_id, key);


--
-- Name: idx_tenants_owner; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_tenants_owner ON public.tenants USING btree (owner_user_id);


--
-- Name: idx_tenants_stripe_customer; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_tenants_stripe_customer ON public.tenants USING btree (stripe_customer_id);


--
-- Name: idx_trend_data_keyword; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_trend_data_keyword ON public.trend_data USING btree (keyword);


--
-- Name: idx_trend_data_rank; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_trend_data_rank ON public.trend_data USING btree (rank);


--
-- Name: idx_trend_data_source_timestamp; Type: INDEX; Schema: public; Owner: neondb_owner
--

CREATE INDEX idx_trend_data_source_timestamp ON public.trend_data USING btree (source, "timestamp");


--
-- Name: access_controls access_controls_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.access_controls
    ADD CONSTRAINT access_controls_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: ad_entities ad_entities_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ad_entities
    ADD CONSTRAINT ad_entities_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: agent_memory agent_memory_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.agent_memory
    ADD CONSTRAINT agent_memory_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: ai_event ai_event_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.ai_event
    ADD CONSTRAINT ai_event_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: api_endpoint api_endpoint_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.api_endpoint
    ADD CONSTRAINT api_endpoint_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: api_endpoints api_endpoints_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.api_endpoints
    ADD CONSTRAINT api_endpoints_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: audit_logs audit_logs_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.audit_logs
    ADD CONSTRAINT audit_logs_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: connected_stores connected_stores_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.connected_stores
    ADD CONSTRAINT connected_stores_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: invite_codes invite_codes_created_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.invite_codes
    ADD CONSTRAINT invite_codes_created_by_fkey FOREIGN KEY (created_by) REFERENCES public."user"(id);


--
-- Name: invite_codes invite_codes_used_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.invite_codes
    ADD CONSTRAINT invite_codes_used_by_fkey FOREIGN KEY (used_by) REFERENCES public."user"(id);


--
-- Name: plugin plugin_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.plugin
    ADD CONSTRAINT plugin_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- Name: product_store product_store_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.product_store
    ADD CONSTRAINT product_store_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: profit_log profit_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.profit_log
    ADD CONSTRAINT profit_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: shopify_order shopify_order_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.shopify_order
    ADD CONSTRAINT shopify_order_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: social_posts social_posts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.social_posts
    ADD CONSTRAINT social_posts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: strategy_cache strategy_cache_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.strategy_cache
    ADD CONSTRAINT strategy_cache_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: subscription subscription_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT subscription_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: team_member team_member_team_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_member
    ADD CONSTRAINT team_member_team_id_fkey FOREIGN KEY (team_id) REFERENCES public.team(id);


--
-- Name: team_member team_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team_member
    ADD CONSTRAINT team_member_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: team team_owner_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.team
    ADD CONSTRAINT team_owner_id_fkey FOREIGN KEY (owner_id) REFERENCES public."user"(id);


--
-- Name: tenant_connections tenant_connections_integration_code_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenant_connections
    ADD CONSTRAINT tenant_connections_integration_code_fkey FOREIGN KEY (integration_code) REFERENCES public.integrations(code);


--
-- Name: tenant_connections tenant_connections_tenant_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenant_connections
    ADD CONSTRAINT tenant_connections_tenant_id_fkey FOREIGN KEY (tenant_id) REFERENCES public.tenants(id);


--
-- Name: tenant_secrets tenant_secrets_connection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenant_secrets
    ADD CONSTRAINT tenant_secrets_connection_id_fkey FOREIGN KEY (connection_id) REFERENCES public.tenant_connections(id);


--
-- Name: tenants tenants_owner_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.tenants
    ADD CONSTRAINT tenants_owner_user_id_fkey FOREIGN KEY (owner_user_id) REFERENCES public."user"(id);


--
-- Name: user_plugin user_plugin_plugin_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_plugin
    ADD CONSTRAINT user_plugin_plugin_id_fkey FOREIGN KEY (plugin_id) REFERENCES public.plugin(id);


--
-- Name: user_plugin user_plugin_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_plugin
    ADD CONSTRAINT user_plugin_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: user_preferences user_preferences_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_preferences
    ADD CONSTRAINT user_preferences_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id) ON DELETE CASCADE;


--
-- Name: user_settings user_settings_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: neondb_owner
--

ALTER TABLE ONLY public.user_settings
    ADD CONSTRAINT user_settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: DEFAULT PRIVILEGES FOR SEQUENCES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON SEQUENCES TO neon_superuser WITH GRANT OPTION;


--
-- Name: DEFAULT PRIVILEGES FOR TABLES; Type: DEFAULT ACL; Schema: public; Owner: cloud_admin
--

ALTER DEFAULT PRIVILEGES FOR ROLE cloud_admin IN SCHEMA public GRANT ALL ON TABLES TO neon_superuser WITH GRANT OPTION;


--
-- PostgreSQL database dump complete
--

