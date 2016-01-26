% Function to obtain phi function

function phi_val = phi(s,t,vertex,var)
	
	if var == 0 && s == vertex
		phi_val = 0 ;
  
	elseif var == 1 && t == vertex
		phi_val = 0 ;
		
	else	
		phi_val = 1 ;
				
	end
