% hard3_0229  eq1=2093 eq2=1890  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(f(f(Y,X),X),f(Z,X)) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(Y,f(X,X)),f(Z,X)) )).
