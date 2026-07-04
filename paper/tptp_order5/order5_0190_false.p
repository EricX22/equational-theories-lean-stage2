% order5_0190  eq1=43581 eq2=51838  gold=None
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( f(X,Y) = f(X,f(f(Z,Y),f(Y,X))) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(f(f(Z,Z),f(X,X)),W) )).
