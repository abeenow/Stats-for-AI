function out = tabulate(A,s,t,w,vertex,burnin_set,its_set)
for i = 1:length(burnin_set)
	for j = 1:length(its_set)
		m = gibbs(A, s, t, w,burnin_set(i),its_set(j));
		out = ['burnin = ',num2str(burnin_set(i)),'-> its = ',num2str(its_set(j)),'{',num2str(m(vertex)),'}'];
		disp(out);
	end
end
