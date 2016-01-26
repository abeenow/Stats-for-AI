function m = gibbs(A, s, t, w, burnin, its)
n = length(A);
sample = randi(2,1,n) - 1; % Generate 1 sample for each vertex randomly and start burnin phase
prob_count = zeros(1,n);

for loop = 1:burnin+its
	
	for resample = 1:n % Assumption : Re-sampling order is from 1st vertex to the nth vertex
		
		phi_prod = 1;
		psi_prod = 1;
	
		resamp_psi_0 = 1;
		resamp_psi_1 = 1;
		
		for i = 1:n 
			% Calculate product of phi's excluding the resample value
			
			if i ~= resample
				phi_prod = phi_prod * phi(s,t,i,sample(i));
			end
			
			for j = i+1:n
			
				if A(i,j) == 1
					
					if i ~= resample
						psi_prod = psi_prod * psi(w,i,j,sample(i),sample(j));
					else
						resamp_psi_0 = resamp_psi_0 * psi(w,i,j,0,sample(j));
						resamp_psi_1 = resamp_psi_1 * psi(w,i,j,1,sample(j));
					end
					
				end
				
			end
		end	

		% Now get prob of sample(resample=0) and sample(resample=1)
		prob_0 = phi(s,t,resample,0) * phi_prod * psi_prod * resamp_psi_0 ;
		prob_1 = phi(s,t,resample,1) * phi_prod * psi_prod * resamp_psi_1 ;
		
		if (prob_0) / ((prob_0) + (prob_1)) > rand(1,1)
			sample(resample) = 0;
		else
			sample(resample) = 1;
		end
		
	end	
	
	if loop > burnin
		prob_count = prob_count + sample ;
	end
	
end
			
m = prob_count / its;
