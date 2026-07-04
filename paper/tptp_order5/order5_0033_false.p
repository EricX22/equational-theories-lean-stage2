% order5_0033  eq1=51259 eq2=34540  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [W,X,Y,Z] : ( f(X,X) = f(f(f(Y,X),f(Z,Z)),W) )).
fof(neg, negated_conjecture, ? [X,Y,Z] : ( X != f(f(f(X,X),f(f(Y,Y),X)),Z) )).
