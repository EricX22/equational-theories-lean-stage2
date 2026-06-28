% hard3_0011  eq1=51 eq2=2862  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(X,f(Y,Z))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(X,f(Y,X)),X),X) )).
