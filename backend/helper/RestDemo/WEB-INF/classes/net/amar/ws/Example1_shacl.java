/******************************************************************************* 
 * Copyright (c) 2020 Eclipse RDF4J contributors.
 * All rights reserved. This program and the accompanying materials
 * are made available under the terms of the Eclipse Distribution License v1.0
 * which accompanies this distribution, and is available at
 * http://www.eclipse.org/org/documents/edl-v10.php.
 *******************************************************************************/
package net.amar.ws;

import java.net.URL;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.Iterator;

import org.eclipse.rdf4j.examples.repository.Example2a_sparql_tsv;
import org.eclipse.rdf4j.model.Model;
import org.eclipse.rdf4j.model.util.ModelBuilder;
import org.eclipse.rdf4j.model.vocabulary.RDF;
import org.eclipse.rdf4j.model.vocabulary.RDF4J;
import org.eclipse.rdf4j.repository.Repository;
import org.eclipse.rdf4j.repository.RepositoryConnection;
import org.eclipse.rdf4j.repository.RepositoryException;
import org.eclipse.rdf4j.repository.sail.SailRepository;
import org.eclipse.rdf4j.rio.RDFFormat;
import org.eclipse.rdf4j.rio.Rio;
import org.eclipse.rdf4j.sail.memory.MemoryStore;
import org.eclipse.rdf4j.sail.shacl.ShaclSail;
import org.eclipse.rdf4j.sail.shacl.ShaclSailValidationException;
import org.json.JSONArray;
import org.json.JSONObject;

import java.net.HttpURLConnection;
import java.net.URI;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.File; // Import the File class
import java.io.FileWriter;
import java.io.IOException; // Import the IOException class to handle errors
import java.util.Scanner;

import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

/**
 * ShaclSail example: load shapes, then data. The data does not conform to the
 * shacl shapes and therefore validation will fail with an exception.
 * 
 * @see https://rdf4j.org/documentation/programming/shacl/
 */

public class Example1_shacl {
	private static HttpURLConnection conn;
	public static OutputStream resultedError = new ByteArrayOutputStream();

	public static void main(String[] args) throws Exception {
		// code of accessing the data from contracting api
		BufferedReader reader;
		String line;
		StringBuffer responseContent = new StringBuffer();
		ArrayList<String> ar = new ArrayList<String>();

		try {
			String query_url = "http://127.0.0.1:5004/contract/term/types";
			URL url = new URL(query_url);
			conn = (HttpURLConnection) url.openConnection();
			// request setup
			conn.setRequestMethod("GET");
			conn.setConnectTimeout(5000);
			conn.setReadTimeout(5000);
			int status = conn.getResponseCode();
			if (status > 299) {
				reader = new BufferedReader(new InputStreamReader(conn.getErrorStream()));
				while ((line = reader.readLine()) != null) {
					responseContent.append(line);
				}
				reader.close();
			} else {
				reader = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				while ((line = reader.readLine()) != null) {
					responseContent.append(line);
				}
				reader.close();
			}
			parse(responseContent.toString());

		} catch (Exception e) {
			System.out.print("error");
			// TODO: handle exception
		} finally {
			conn.disconnect();
		}

		ShaclSail shaclSail = new ShaclSail(new MemoryStore());
		Repository sailRepository = new SailRepository(shaclSail);

//		URL shaclRules = Example2a_sparql_tsv.class.getResource("/shacl-shapes.ttl");
		URL shaclRules = Example2a_sparql_tsv.class.getResource("/smashHit-contract-shaps-graph.ttl");

		File myObj = new File("\\RestDemo\\src\\main\\resources\\type-validation.ttl");
		System.out.println("path: " + myObj);
		URL data = myObj.toURL();

//		URL data = Example2a_sparql_tsv.class.getResource("/example-data-artists-invalid.ttl");

		try (RepositoryConnection connection = sailRepository.getConnection()) {

			connection.add(shaclRules.openStream(), "", RDFFormat.TURTLE, RDF4J.SHACL_SHAPE_GRAPH);
			connection.add(data.openStream(), data.toExternalForm(), RDFFormat.TURTLE);

		} catch (RepositoryException exception) {
			Throwable cause = exception.getCause();
			if (cause instanceof ShaclSailValidationException) {
				System.out.println("Validation failed!");
				Model validationReportModel = ((ShaclSailValidationException) cause).validationReportAsModel();
				Rio.write(validationReportModel, resultedError, RDFFormat.TURTLE);
				System.out.println("hi in main class " + resultedError);
			} else {
				throw exception;
			}
		}

	}

	public static OutputStream myMethod() {
		System.out.println("hi" + resultedError);
		return Example1_shacl.resultedError;
	}

	public static String parse(String responseBody) {
		JSONArray termTypes = new JSONArray(responseBody);
		for (int i = 0; i < termTypes.length(); i++) {
			JSONObject termType = termTypes.getJSONObject(i);
			String termTypeId = termType.getString("termTypeId");
			String name = termType.getString("name");
			String description = termType.getString("description");

			System.out.print(termTypeId + " " + name + " " + description);

			ModelBuilder builder = new ModelBuilder();
			Model termTypeModel = builder.setNamespace("ex", "http://example.org/")
					.setNamespace("core", "http://ontologies.atb-bremen.de/smashHitCore#")
					.setNamespace("dc", "http://purl.org/dc/elements/1.1/")
					.setNamespace("fn", "http://www.w3.org/2005/xpath-functions#")
					.setNamespace("gn", "http://www.geonames.org/ontology#")
					.setNamespace("LCC", "https://www.omg.org/spec/LCC/Countries/CountryRepresentation/")
					.setNamespace("dct", "http://purl.org/dc/terms/").setNamespace("dpv", "http://www.w3.org/ns/dpv#")
					.setNamespace("owl", "http://www.w3.org/2002/07/owl#")
					.setNamespace("rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#")
					.setNamespace("xml", "http://www.w3.org/XML/1998/namespace")
					.setNamespace("xsd", "http://www.w3.org/2001/XMLSchema#")
					.setNamespace("dcat", "http://www.w3.org/ns/dcat#")
					.setNamespace("foaf", "http://xmlns.com/foaf/0.1/")
					.setNamespace("odrl", "http://www.w3.org/ns/odrl/2/")
					.setNamespace("prov", "http://www.w3.org/ns/prov#")
					.setNamespace("rdfs", "http://www.w3.org/2000/01/rdf-schema#")
					.setNamespace("skos", "http://www.w3.org/2004/02/skos/core#")
					.setNamespace("time", "http://www.w3.org/2006/time#")
					.setNamespace("grddl", "http://www.w3.org/2003/g/data-view#")
					.setNamespace("rdf4j", "http://rdf4j.org/schema/rdf4j#")
					.setNamespace("prov-o", "%20https://www.w3.org/TR/prov-o#")
					.setNamespace("sesame", "http://www.openrdf.org/schema/sesame#")
					.setNamespace("consent", "http://purl.org/adaptcentre/openscience/ontologies/consent#")
					.setNamespace("dpv-gdpr", "http://www.w3.org/ns/dpv-gdpr#")
					.setNamespace("gconsent", "https://w3id.org/GConsent#")
					.setNamespace("security", "http://ontologies.atb-bremen.de/security#")
					.setNamespace("fibo-der-dc-dma",
							"https://spec.edmcouncil.org/fibo/ontology/DER/DerivativesContracts/DerivativesMasterAgreements/")
					.setNamespace("fibo-fbc-fe-fse",
							"https://spec.edmcouncil.org/fibo/ontology/FBC/FunctionalEntities/FinancialServicesEntities/")
					.setNamespace("fibo-fbc-dae-dbt",
							"https://spec.edmcouncil.org/fibo/ontology/FBC/DebtAndEquities/Debt/")
					.setNamespace("fibo-fnd-agr-ctr",
							"https://spec.edmcouncil.org/fibo/ontology/FND/Agreements/Contracts/")
					.setNamespace("fibo-fnd-plc-loc", "https://spec.edmcouncil.org/fibo/ontology/FND/Places/Locations/")
					.setNamespace("fibo-fnd-trext-reatr",
							"https://spec.edmcouncil.org/fibo/ontology/FND/TransactionsExt/REATransactions/")
					.setNamespace("fibo-loan-loant-mloan",
							"https://spec.edmcouncil.org/fibo/ontology/LOAN/LoanTypes/MortgageLoans/")

					.subject("core:" + termTypeId).add("rdf:type", "core:TermTypes").add("core:typeID", termTypeId)
					.add("core:hasName", "").add("dct:description", description).build();

			try {
				File myObj = new File("\\RestDemo\\src\\main\\resources\\type-validation.ttl");
				if (myObj.createNewFile()) {
					OutputStream stream = new ByteArrayOutputStream();
					FileWriter myWriter = new FileWriter(myObj);
					Rio.write(termTypeModel, stream, RDFFormat.TURTLE);
					myWriter.write(stream.toString());
					myWriter.close();
				} else {
					myObj.delete();
					File myObj1 = new File("\\RestDemo\\src\\main\\resources\\type-validation.ttl");
					myObj1.createNewFile();
					OutputStream stream1 = new ByteArrayOutputStream();
					FileWriter myWriter = new FileWriter(myObj1);
					Rio.write(termTypeModel, stream1, RDFFormat.TURTLE);
					myWriter.write(stream1.toString());
					myWriter.close();
				}
			} catch (IOException e) {
				System.out.println("An error occurred.");
				e.printStackTrace();
			}

		}

		return null;
	}
}
