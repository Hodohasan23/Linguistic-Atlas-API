--
-- PostgreSQL database dump
--

\restrict egYk3WPLNCkyK4bPpCmpp4Apvl5HXERONnEIQBCru7Q4ufh32l75F16u8SFVAdO

-- Dumped from database version 14.19 (Homebrew)
-- Dumped by pg_dump version 14.19 (Homebrew)

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
-- Name: code; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.code (
    id character varying NOT NULL,
    parameter_id character varying,
    name character varying,
    description character varying,
    numerical_value double precision
);


ALTER TABLE public.code OWNER TO hodohasan;

--
-- Name: language; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.language (
    id character varying NOT NULL,
    name character varying NOT NULL,
    macroarea character varying,
    latitude double precision,
    longitude double precision,
    glottocode character varying,
    iso_code character varying,
    level character varying,
    countries character varying,
    family_id character varying,
    language_id character varying,
    closest_iso_code character varying,
    first_year_of_documentation integer,
    last_year_of_documentation integer,
    is_isolate boolean
);


ALTER TABLE public.language OWNER TO hodohasan;

--
-- Name: languagename; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.languagename (
    id integer NOT NULL,
    source_id character varying NOT NULL,
    language_id character varying NOT NULL,
    name character varying NOT NULL,
    provider character varying,
    lang character varying
);


ALTER TABLE public.languagename OWNER TO hodohasan;

--
-- Name: languagename_id_seq; Type: SEQUENCE; Schema: public; Owner: hodohasan
--

CREATE SEQUENCE public.languagename_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.languagename_id_seq OWNER TO hodohasan;

--
-- Name: languagename_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hodohasan
--

ALTER SEQUENCE public.languagename_id_seq OWNED BY public.languagename.id;


--
-- Name: languageset; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.languageset (
    id integer NOT NULL,
    user_id integer NOT NULL,
    title character varying NOT NULL,
    description character varying,
    notes character varying,
    created_at timestamp without time zone NOT NULL,
    updated_at timestamp without time zone NOT NULL
);


ALTER TABLE public.languageset OWNER TO hodohasan;

--
-- Name: languageset_id_seq; Type: SEQUENCE; Schema: public; Owner: hodohasan
--

CREATE SEQUENCE public.languageset_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.languageset_id_seq OWNER TO hodohasan;

--
-- Name: languageset_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hodohasan
--

ALTER SEQUENCE public.languageset_id_seq OWNED BY public.languageset.id;


--
-- Name: languagesetitem; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.languagesetitem (
    id integer NOT NULL,
    language_set_id integer NOT NULL,
    language_id character varying NOT NULL
);


ALTER TABLE public.languagesetitem OWNER TO hodohasan;

--
-- Name: languagesetitem_id_seq; Type: SEQUENCE; Schema: public; Owner: hodohasan
--

CREATE SEQUENCE public.languagesetitem_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.languagesetitem_id_seq OWNER TO hodohasan;

--
-- Name: languagesetitem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hodohasan
--

ALTER SEQUENCE public.languagesetitem_id_seq OWNED BY public.languagesetitem.id;


--
-- Name: media; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.media (
    id character varying NOT NULL,
    name character varying,
    description character varying,
    media_type character varying,
    download_url character varying,
    path_in_zip character varying
);


ALTER TABLE public.media OWNER TO hodohasan;

--
-- Name: parameter; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.parameter (
    id character varying NOT NULL,
    name character varying NOT NULL,
    description character varying,
    column_spec character varying,
    type character varying,
    info_url character varying,
    datatype character varying,
    source character varying
);


ALTER TABLE public.parameter OWNER TO hodohasan;

--
-- Name: parametervalue; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.parametervalue (
    id character varying NOT NULL,
    language_id character varying NOT NULL,
    parameter_id character varying NOT NULL,
    value character varying,
    code_id character varying,
    comment character varying,
    source character varying,
    code_reference character varying
);


ALTER TABLE public.parametervalue OWNER TO hodohasan;

--
-- Name: setcomparison; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.setcomparison (
    id integer NOT NULL,
    user_id integer NOT NULL,
    set_a_id integer NOT NULL,
    set_b_id integer NOT NULL,
    summary character varying,
    created_at timestamp without time zone NOT NULL
);


ALTER TABLE public.setcomparison OWNER TO hodohasan;

--
-- Name: setcomparison_id_seq; Type: SEQUENCE; Schema: public; Owner: hodohasan
--

CREATE SEQUENCE public.setcomparison_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.setcomparison_id_seq OWNER TO hodohasan;

--
-- Name: setcomparison_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hodohasan
--

ALTER SEQUENCE public.setcomparison_id_seq OWNED BY public.setcomparison.id;


--
-- Name: tree; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public.tree (
    id character varying NOT NULL,
    name character varying,
    description character varying,
    tree_is_rooted boolean,
    tree_type character varying,
    tree_branch_length_unit character varying,
    media_id character varying,
    source character varying
);


ALTER TABLE public.tree OWNER TO hodohasan;

--
-- Name: user; Type: TABLE; Schema: public; Owner: hodohasan
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying NOT NULL,
    email character varying NOT NULL,
    password_hash character varying NOT NULL,
    role character varying NOT NULL
);


ALTER TABLE public."user" OWNER TO hodohasan;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: hodohasan
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO hodohasan;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hodohasan
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: languagename id; Type: DEFAULT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languagename ALTER COLUMN id SET DEFAULT nextval('public.languagename_id_seq'::regclass);


--
-- Name: languageset id; Type: DEFAULT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languageset ALTER COLUMN id SET DEFAULT nextval('public.languageset_id_seq'::regclass);


--
-- Name: languagesetitem id; Type: DEFAULT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languagesetitem ALTER COLUMN id SET DEFAULT nextval('public.languagesetitem_id_seq'::regclass);


--
-- Name: setcomparison id; Type: DEFAULT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.setcomparison ALTER COLUMN id SET DEFAULT nextval('public.setcomparison_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Name: code code_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.code
    ADD CONSTRAINT code_pkey PRIMARY KEY (id);


--
-- Name: language language_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.language
    ADD CONSTRAINT language_pkey PRIMARY KEY (id);


--
-- Name: languagename languagename_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languagename
    ADD CONSTRAINT languagename_pkey PRIMARY KEY (id);


--
-- Name: languageset languageset_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languageset
    ADD CONSTRAINT languageset_pkey PRIMARY KEY (id);


--
-- Name: languagesetitem languagesetitem_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languagesetitem
    ADD CONSTRAINT languagesetitem_pkey PRIMARY KEY (id);


--
-- Name: media media_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.media
    ADD CONSTRAINT media_pkey PRIMARY KEY (id);


--
-- Name: parameter parameter_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.parameter
    ADD CONSTRAINT parameter_pkey PRIMARY KEY (id);


--
-- Name: parametervalue parametervalue_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.parametervalue
    ADD CONSTRAINT parametervalue_pkey PRIMARY KEY (id);


--
-- Name: setcomparison setcomparison_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.setcomparison
    ADD CONSTRAINT setcomparison_pkey PRIMARY KEY (id);


--
-- Name: tree tree_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.tree
    ADD CONSTRAINT tree_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_code_name; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_code_name ON public.code USING btree (name);


--
-- Name: ix_code_parameter_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_code_parameter_id ON public.code USING btree (parameter_id);


--
-- Name: ix_language_family_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_language_family_id ON public.language USING btree (family_id);


--
-- Name: ix_language_glottocode; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_language_glottocode ON public.language USING btree (glottocode);


--
-- Name: ix_language_iso_code; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_language_iso_code ON public.language USING btree (iso_code);


--
-- Name: ix_language_language_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_language_language_id ON public.language USING btree (language_id);


--
-- Name: ix_language_level; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_language_level ON public.language USING btree (level);


--
-- Name: ix_language_macroarea; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_language_macroarea ON public.language USING btree (macroarea);


--
-- Name: ix_language_name; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_language_name ON public.language USING btree (name);


--
-- Name: ix_languagename_language_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_languagename_language_id ON public.languagename USING btree (language_id);


--
-- Name: ix_languagename_name; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_languagename_name ON public.languagename USING btree (name);


--
-- Name: ix_languagename_source_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_languagename_source_id ON public.languagename USING btree (source_id);


--
-- Name: ix_languageset_title; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_languageset_title ON public.languageset USING btree (title);


--
-- Name: ix_languageset_user_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_languageset_user_id ON public.languageset USING btree (user_id);


--
-- Name: ix_languagesetitem_language_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_languagesetitem_language_id ON public.languagesetitem USING btree (language_id);


--
-- Name: ix_languagesetitem_language_set_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_languagesetitem_language_set_id ON public.languagesetitem USING btree (language_set_id);


--
-- Name: ix_media_media_type; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_media_media_type ON public.media USING btree (media_type);


--
-- Name: ix_parameter_name; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_parameter_name ON public.parameter USING btree (name);


--
-- Name: ix_parameter_type; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_parameter_type ON public.parameter USING btree (type);


--
-- Name: ix_parametervalue_code_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_parametervalue_code_id ON public.parametervalue USING btree (code_id);


--
-- Name: ix_parametervalue_language_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_parametervalue_language_id ON public.parametervalue USING btree (language_id);


--
-- Name: ix_parametervalue_parameter_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_parametervalue_parameter_id ON public.parametervalue USING btree (parameter_id);


--
-- Name: ix_setcomparison_set_a_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_setcomparison_set_a_id ON public.setcomparison USING btree (set_a_id);


--
-- Name: ix_setcomparison_set_b_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_setcomparison_set_b_id ON public.setcomparison USING btree (set_b_id);


--
-- Name: ix_setcomparison_user_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_setcomparison_user_id ON public.setcomparison USING btree (user_id);


--
-- Name: ix_tree_media_id; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_tree_media_id ON public.tree USING btree (media_id);


--
-- Name: ix_tree_name; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_tree_name ON public.tree USING btree (name);


--
-- Name: ix_tree_tree_type; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_tree_tree_type ON public.tree USING btree (tree_type);


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_role; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE INDEX ix_user_role ON public."user" USING btree (role);


--
-- Name: ix_user_username; Type: INDEX; Schema: public; Owner: hodohasan
--

CREATE UNIQUE INDEX ix_user_username ON public."user" USING btree (username);


--
-- Name: code code_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.code
    ADD CONSTRAINT code_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.parameter(id);


--
-- Name: languagename languagename_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languagename
    ADD CONSTRAINT languagename_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.language(id);


--
-- Name: languageset languageset_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languageset
    ADD CONSTRAINT languageset_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: languagesetitem languagesetitem_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languagesetitem
    ADD CONSTRAINT languagesetitem_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.language(id);


--
-- Name: languagesetitem languagesetitem_language_set_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.languagesetitem
    ADD CONSTRAINT languagesetitem_language_set_id_fkey FOREIGN KEY (language_set_id) REFERENCES public.languageset(id);


--
-- Name: parametervalue parametervalue_code_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.parametervalue
    ADD CONSTRAINT parametervalue_code_id_fkey FOREIGN KEY (code_id) REFERENCES public.code(id);


--
-- Name: parametervalue parametervalue_language_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.parametervalue
    ADD CONSTRAINT parametervalue_language_id_fkey FOREIGN KEY (language_id) REFERENCES public.language(id);


--
-- Name: parametervalue parametervalue_parameter_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.parametervalue
    ADD CONSTRAINT parametervalue_parameter_id_fkey FOREIGN KEY (parameter_id) REFERENCES public.parameter(id);


--
-- Name: setcomparison setcomparison_set_a_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.setcomparison
    ADD CONSTRAINT setcomparison_set_a_id_fkey FOREIGN KEY (set_a_id) REFERENCES public.languageset(id);


--
-- Name: setcomparison setcomparison_set_b_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.setcomparison
    ADD CONSTRAINT setcomparison_set_b_id_fkey FOREIGN KEY (set_b_id) REFERENCES public.languageset(id);


--
-- Name: setcomparison setcomparison_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.setcomparison
    ADD CONSTRAINT setcomparison_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- Name: tree tree_media_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hodohasan
--

ALTER TABLE ONLY public.tree
    ADD CONSTRAINT tree_media_id_fkey FOREIGN KEY (media_id) REFERENCES public.media(id);


--
-- PostgreSQL database dump complete
--

\unrestrict egYk3WPLNCkyK4bPpCmpp4Apvl5HXERONnEIQBCru7Q4ufh32l75F16u8SFVAdO

