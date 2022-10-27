package net.amar.ws;


import jakarta.ws.rs.GET;
import jakarta.ws.rs.Path;
import jakarta.ws.rs.Produces;
import jakarta.ws.rs.core.MediaType;

import java.io.OutputStream;

import org.eclipse.rdf4j.examples.shacl.*;

@Path("/publish")
public class HelloResource {
	
	@GET
	@Produces(MediaType.TEXT_PLAIN)
	public String getString() {
		OutputStream result=Example1_shacl.myMethod();
		System.out.println(result);
		return "hello world how are you?";
		
	}
}
