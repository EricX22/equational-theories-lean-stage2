% order5_0139  eq1=61069 eq2=5159  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(f(X,Y),X) = f(f(Y,f(X,Z)),X) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(Y,f(Y,f(Z,f(Z,f(X,Z))))) )).
