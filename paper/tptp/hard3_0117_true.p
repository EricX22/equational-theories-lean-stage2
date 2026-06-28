% hard3_0117  eq1=943 eq2=3962  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(Z,X),f(X,X))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(Y,f(Y,X)),Y) )).
