% hard3_0110  eq1=885 eq2=2939  gold=False
% FALSE-direction: find counterexample magma
fof(hyp, axiom,             ! [X,Y,Z] : ( X = f(Y,f(f(X,Y),f(Z,X))) )).
fof(neg, negated_conjecture, ? [X,Y] : ( X != f(f(f(Y,f(Y,X)),Y),X) )).
