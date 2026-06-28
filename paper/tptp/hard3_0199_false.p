% hard3_0199  eq1=1844 eq2=2448  gold=True
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(X,f(X,Y)),f(Z,Y)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(X,f(f(X,Y),X)),Z) )).
