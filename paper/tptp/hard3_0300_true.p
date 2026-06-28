% hard3_0300  eq1=2848 eq2=1063  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y] : ( X = f(f(f(X,f(X,X)),X),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,f(Z,Z)),X)) )).
