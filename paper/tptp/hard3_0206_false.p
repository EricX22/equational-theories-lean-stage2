% hard3_0206  eq1=1924 eq2=3338  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y] : ( X = f(f(Y,f(Y,X)),f(Y,X)) )).
fof(neg, negated_conjecture, ? [W,X,Y,Z] : ( f(X,Y) != f(X,f(Z,f(W,Y))) )).
