% hard3_0294  eq1=2787 eq2=3007  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(Y,X)),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,Z)),X),X) )).
