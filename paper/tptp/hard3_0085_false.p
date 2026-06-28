% hard3_0085  eq1=644 eq2=2462  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(X,f(Y,f(f(Y,Y),Z))) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(f(Y,X),Z)),X) )).
