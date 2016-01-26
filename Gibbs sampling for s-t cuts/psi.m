% Function to obtain psi function

function psi_val = psi(weight,vertex1,vertex2,var1,var2)
	
	if var1 ~= var2
		psi_val = weight(vertex1,vertex2) ;
	else
		psi_val = 1 ;
	end
