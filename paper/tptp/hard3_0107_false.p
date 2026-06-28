% hard3_0107  eq1=859 eq2=2878  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(X,f(f(Y,Z),f(Y,W))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,f(Y,Y)),Z),X) )).
