--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4
-- Dumped by pg_dump version 15.4

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
-- Name: address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.address (
    member_user_id integer NOT NULL,
    house_number integer NOT NULL,
    street character varying(100) NOT NULL,
    town character varying(100) NOT NULL
);


ALTER TABLE public.address OWNER TO postgres;

--
-- Name: appointment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.appointment (
    appointment_id integer NOT NULL,
    caregiver_user_id integer NOT NULL,
    member_user_id integer NOT NULL,
    appointment_date timestamp without time zone NOT NULL,
    appointment_time time without time zone NOT NULL,
    work_hours double precision NOT NULL,
    status character varying(30) NOT NULL,
    CONSTRAINT appointment_status_check CHECK (((status)::text = ANY ((ARRAY['confirmed'::character varying, 'declined'::character varying, 'waiting'::character varying])::text[])))
);


ALTER TABLE public.appointment OWNER TO postgres;

--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.appointment_appointment_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.appointment_appointment_id_seq OWNER TO postgres;

--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.appointment_appointment_id_seq OWNED BY public.appointment.appointment_id;


--
-- Name: caregiver; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.caregiver (
    caregiver_user_id integer NOT NULL,
    photo character varying(100) NOT NULL,
    gender character varying(20) NOT NULL,
    caregiving_type character varying(50) NOT NULL,
    hourly_rate double precision NOT NULL,
    CONSTRAINT checkforcaretype CHECK (((caregiving_type)::text = ANY ((ARRAY['babysitter'::character varying, 'caregiver for elderly'::character varying, 'playmate for children'::character varying])::text[])))
);


ALTER TABLE public.caregiver OWNER TO postgres;

--
-- Name: job; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job (
    job_id integer NOT NULL,
    member_user_id integer NOT NULL,
    required_caregiving_type character varying(50) NOT NULL,
    other_requirements text,
    date_posted timestamp without time zone NOT NULL,
    CONSTRAINT checkforcaretype CHECK (((required_caregiving_type)::text = ANY ((ARRAY['babysitter'::character varying, 'caregiver for elderly'::character varying, 'playmate for children'::character varying])::text[])))
);


ALTER TABLE public.job OWNER TO postgres;

--
-- Name: job_application; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.job_application (
    job_id integer NOT NULL,
    caregiver_user_id integer NOT NULL,
    date_applied timestamp without time zone NOT NULL
);


ALTER TABLE public.job_application OWNER TO postgres;

--
-- Name: job_job_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.job_job_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.job_job_id_seq OWNER TO postgres;

--
-- Name: job_job_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.job_job_id_seq OWNED BY public.job.job_id;


--
-- Name: member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member (
    member_user_id integer NOT NULL,
    house_rules text
);


ALTER TABLE public.member OWNER TO postgres;

--
-- Name: user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public."user" (
    user_id integer NOT NULL,
    email character varying(100) NOT NULL,
    given_name character varying(100) NOT NULL,
    surname character varying(100) NOT NULL,
    city character varying(100) NOT NULL,
    phone_number character varying(100) NOT NULL,
    profile_description text,
    password character varying(100) NOT NULL
);


ALTER TABLE public."user" OWNER TO postgres;

--
-- Name: user_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.user_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_user_id_seq OWNER TO postgres;

--
-- Name: user_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.user_user_id_seq OWNED BY public."user".user_id;


--
-- Name: appointment appointment_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment ALTER COLUMN appointment_id SET DEFAULT nextval('public.appointment_appointment_id_seq'::regclass);


--
-- Name: job job_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job ALTER COLUMN job_id SET DEFAULT nextval('public.job_job_id_seq'::regclass);


--
-- Name: user user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user" ALTER COLUMN user_id SET DEFAULT nextval('public.user_user_id_seq'::regclass);


--
-- Data for Name: address; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.address (member_user_id, house_number, street, town) FROM stdin;
11	1	Buran street	Astana
9	4	Kabanbay Batyr street	Astana
4	2	Buran street	Astana
5	5	Kabanbay Batyr street	Almaty
6	6	Pushikina street	Moscow
17	7	Orynbor street	Astana
18	8	Saryarka street	Astana
19	9	Mangyluk street	Astana
20	10	Mangyluk street	Astana
\.


--
-- Data for Name: appointment; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.appointment (appointment_id, caregiver_user_id, member_user_id, appointment_date, appointment_time, work_hours, status) FROM stdin;
1	10	9	2024-03-01 00:00:00	12:00:00	7	confirmed
2	8	9	2024-02-01 00:00:00	12:00:00	1	confirmed
3	1	4	2024-02-01 00:00:00	13:00:00	2	confirmed
4	3	4	2024-04-01 00:00:00	12:00:00	1	declined
7	3	11	2024-02-01 00:00:00	15:00:00	5	confirmed
8	7	5	2024-03-01 00:00:00	12:00:00	13	declined
9	7	6	2024-03-01 00:00:00	12:00:00	4	confirmed
10	1	11	2024-02-01 00:00:00	12:00:00	1	confirmed
\.


--
-- Data for Name: caregiver; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.caregiver (caregiver_user_id, photo, gender, caregiving_type, hourly_rate) FROM stdin;
15	abpba9	female	playmate for children	10.01
16	abpba10	male	playmate for children	22
1	abpba1	male	babysitter	1
10	abpba3	female	babysitter	1.4
8	abpba5	male	caregiver for elderly	3.5
7	abpba4	female	babysitter	2.5
3	abpba2	male	babysitter	2
12	abpba6	female	caregiver for elderly	4.5
13	abpba7	female	caregiver for elderly	0.6
14	abpba8	male	playmate for children	9.1
\.


--
-- Data for Name: job; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.job (job_id, member_user_id, required_caregiving_type, other_requirements, date_posted) FROM stdin;
4	9	babysitter	WE HATE DOGS	2023-01-13 07:10:23
5	4	babysitter	Be gentle with the child	2023-11-01 05:35:40
6	4	playmate for children	He is adopted, be nice	2023-05-10 02:42:40
7	4	babysitter	Be gentle, be smart. be good	2023-03-07 00:00:00
\.


--
-- Data for Name: job_application; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.job_application (job_id, caregiver_user_id, date_applied) FROM stdin;
5	8	2024-01-02 00:00:00
5	7	2024-01-01 00:00:00
6	7	2024-01-13 00:00:00
\.


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.member (member_user_id, house_rules) FROM stdin;
11	No pets. No food
9	Yes pets please i like cats.
4	Be clean. Be gentle. Be smart
2	No pets allowed in the house
5	I love pets, especially dogs
6	No music
17	Be quite
18	MAKE SOME NOISE
19	No pets no 
20	THERE IS NO RULES!!!
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public."user" (user_id, email, given_name, surname, city, phone_number, profile_description, password) FROM stdin;
1	bolat1@gmail.com	Jonh	Bolatov	Astana	88005553535	Cool guy	123
2	email13@gmail.com	Antio	Rodriges	Mexico	+666666666	Professional dota 2 player	12312312312312
3	email1@gmail.com	Bolat	Familiya	Almaty	+77039284955	Very handsome	12311111
4	email12@gmail.com	JeiJei	Kennedy	New York	+732321321	I like chicken kebab	1238806957056
5	email15@gmail.com	Jessy	Pinkman	Kokshetay	+3221312312	Hello. I know chemistry	13
6	email16@gmail.com	Saul	Goodman	Astana	+2227743849523	Where am I	9
7	email3@gmail.com	Askar	Bolatov	Astana	+9999999999	Bolat bolatov is my brother	123111111111111111111
8	email4@gmail.com	Ivan	Ivanov	Kokshetay	+3213219999	Hello i am Ivan	1231111113
9	email14@gmail.com	Anton	Dyrachyo	Almaty	+12345679	Professional Dota 2 player. Major winner. Best carry in the world	12301
11	email11@gmail.com	Bolat	Bolatov	Moscow	8832323122	I am from Russia	1000000000000
12	email5@gmail.com	Asem	Asemova	Astana	+7743849523	Where am I	12000001
13	email6@gmail.com	Asem	Bolatov	Almaty	+999993123129999	Bolat bolatov is my brother	12300001111111111
14	email7@gmail.com	Bolatbeek	Ashura	Astana	+9777832159	Bolat bolatov is not my brother	00234511111111
15	email8@gmail.com	Asuka	Thanos	Astana	+111134953	Ok	012311110
16	email9@gmail.com	Asuka	Bolatov	Astana	+9999012349	Bolat bolatov is my brother	1
17	email17@gmail.com	Korol	Arthas	Almaty	+99129999	Best in the world	12345678
18	email18@gmail.com	Wraith	King	Astana	+9772159	Arthas is my brother	00234511111
19	email19@gmail.com	Rost1k	Earth	Astana	+111111134953	NS	0120
20	email20@gmail.com	Nix	Fruit	Astana	+012349	I eat only fruits	19
10	email2@gmail.com	Askar	Askarov	Astana	+77771010001	Professional footbal player	12312312312312
\.


--
-- Name: appointment_appointment_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.appointment_appointment_id_seq', 10, true);


--
-- Name: job_job_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.job_job_id_seq', 10, true);


--
-- Name: user_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.user_user_id_seq', 20, true);


--
-- Name: address address_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_pkey PRIMARY KEY (member_user_id);


--
-- Name: appointment appointment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_pkey PRIMARY KEY (appointment_id);


--
-- Name: caregiver caregiver_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caregiver
    ADD CONSTRAINT caregiver_pkey PRIMARY KEY (caregiver_user_id);


--
-- Name: job_application job_application_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_application
    ADD CONSTRAINT job_application_pkey PRIMARY KEY (job_id, caregiver_user_id);


--
-- Name: job job_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_pkey PRIMARY KEY (job_id);


--
-- Name: member member_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_pkey PRIMARY KEY (member_user_id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_phone_number_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_phone_number_key UNIQUE (phone_number);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (user_id);


--
-- Name: address address_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.address
    ADD CONSTRAINT address_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public.member(member_user_id);


--
-- Name: appointment appointment_caregiver_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_caregiver_user_id_fkey FOREIGN KEY (caregiver_user_id) REFERENCES public.caregiver(caregiver_user_id);


--
-- Name: appointment appointment_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.appointment
    ADD CONSTRAINT appointment_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public.member(member_user_id);


--
-- Name: caregiver caregiver_caregiver_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.caregiver
    ADD CONSTRAINT caregiver_caregiver_user_id_fkey FOREIGN KEY (caregiver_user_id) REFERENCES public."user"(user_id);


--
-- Name: job_application job_application_caregiver_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_application
    ADD CONSTRAINT job_application_caregiver_user_id_fkey FOREIGN KEY (caregiver_user_id) REFERENCES public.caregiver(caregiver_user_id);


--
-- Name: job_application job_application_job_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job_application
    ADD CONSTRAINT job_application_job_id_fkey FOREIGN KEY (job_id) REFERENCES public.job(job_id);


--
-- Name: job job_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.job
    ADD CONSTRAINT job_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public.member(member_user_id);


--
-- Name: member member_member_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_member_user_id_fkey FOREIGN KEY (member_user_id) REFERENCES public."user"(user_id);


--
-- PostgreSQL database dump complete
--

