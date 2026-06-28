% hard3_0219  eq1=2059 eq2=3077  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( X = f(f(f(X,Y),X),f(Z,W)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(f(X,Y),Y),X),Z) )).
